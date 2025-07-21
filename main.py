from typing import List
from typing import Optional
from fastapi import FastAPI,status, Query
from pydantic import BaseModel
from bson.objectid import ObjectId  # to handle ObjectId from MongoDB
from db import collection, get_next_id, orders_collection   # import collection from db.py


app = FastAPI()

class SizeQuantity(BaseModel):
    size: str
    quantity: int

class Item(BaseModel):
    name: str
    price: float
    sizes: SizeQuantity

# Each item in an order
class OrderItem(BaseModel):
    productId: str
    qty: int

# Whole order
class Order(BaseModel):
    userId: str
    items: List[OrderItem]

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Utility to serialize MongoDB docs
def serialize_product(doc):
    return {
        "id": doc.get("id"),  # our custom incremental id
        "name": doc.get("name"),
        "price": doc.get("price"),
    }

@app.post("/products", status_code=status.HTTP_201_CREATED)
async def products(item: Item):
    # Get the next custom id
    next_id = get_next_id()

    # Convert Pydantic model to dict and add id
    item_dict = item.dict()
    item_dict["id"] = next_id

    # Insert into MongoDB
    collection.insert_one(item_dict)
    return {"id": "1234567890"}



@app.get("/products")
async def list_products(
    name: Optional[str] = Query(None, description="Partial search on product name"),
    size: Optional[str] = Query(None, description="Filter by size"),
    limit: int = Query(10, ge=1, le=100, description="Number of documents to return"),
    offset: int = Query(0, ge=0, description="Number of documents to skip"),
):
    query = {}

    # filter by partial name using regex (case-insensitive)
    if name:
        query["name"] = {"$regex": name, "$options": "i"}

    # filter by size field
    if size:
        query["sizes.size"] = size

     # total matching documents
    total_count = collection.count_documents(query)

    # MongoDB query with pagination
    cursor = (
        collection.find(query)
        .sort("_id", 1)  # sort by MongoDB _id
        .skip(offset)
        .limit(limit)
    )

    products = [serialize_product(doc) for doc in cursor]

     # calculate next and previous offsets
    next_offset = offset + limit if (offset + limit) < total_count else None
    previous_offset = offset - limit if (offset - limit) >= 0 else None

    return {
        "data": products,
        "page": {
            "next": next_offset,
            "limit": limit,
            "previous": previous_offset
        }
    }

@app.post("/orders", status_code=status.HTTP_201_CREATED)
async def create_order(order: Order):
    # Convert Pydantic model to dict
    order_dict = order.dict()

    # Optionally, add timestamp or orderId
    # Example: using Mongo ObjectId as unique order id
    result = orders_collection.insert_one(order_dict)

    return {"id": "1234567890"}

@app.get("/orders/{user_id}")
async def list_orders(
    user_id: str,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    # filter by userId
    query = {"userId": user_id}
    total_count = orders_collection.count_documents(query)

    cursor = (
        orders_collection.find(query)
        .sort("_id", 1)
        .skip(offset)
        .limit(limit)
    )

    enriched_orders = []

    for order in cursor:
        order_items = []
        total_amount = 0.0

        for item in order.get("items", []):
            product_id = item.get("productId")
            qty = item.get("qty", 0)

            # lookup product details from products collection
            product = collection.find_one({"id": int(product_id)})
            if not product:
                continue

            product_name = product.get("name")
            product_price = product.get("price", 0.0)

            total_amount += product_price * qty

            order_items.append({
                "productdetails": {
                    "name": product_name,
                    "id": str(product.get("id"))
                },
                "qty": qty
            })

        enriched_orders.append({
            "id": str(order.get("id") if "id" in order else order.get("_id")),
            "item": order_items,
            "total": total_amount
        })

    next_offset = offset + limit if (offset + limit) < total_count else None
    previous_offset = offset - limit if (offset - limit) >= 0 else None

    return {
        "data": enriched_orders,
        "page": {
            "next": next_offset,
            "limit": limit,
            "previous": previous_offset
        }
    }