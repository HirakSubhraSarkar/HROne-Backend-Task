# 🛒 FastAPI + MongoDB Product & Order Management API

A simple **Product and Order Management REST API** built with **FastAPI** and **MongoDB (Atlas)**.  
Supports product creation, listing with pagination and filters, order creation, and listing of orders with enriched product details.

---

## ✨ Features

✅ Create products with auto-increment custom IDs  
✅ List products with:
- Partial name search (regex)
- Size filter
- Pagination (limit/offset with `next` & `previous`)  

✅ Create orders with multiple items  
✅ Get orders for a user with enriched product details and total amount  
✅ Fully connected to MongoDB Atlas with a custom sequence counter

---

## ⚡ Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) (Python web framework)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (Cloud database)
- [PyMongo](https://pymongo.readthedocs.io/) (MongoDB client)
- Uvicorn (ASGI server)

---

## 📦 Installation (Local)

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### 2. Create a virtual environment and activate
```bash
python3 -m venv myenv
source myenv/bin/activate     # Linux/Mac
# OR
myenv\Scripts\activate        # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your environment
In `db.py`, configure your MongoDB URI (Atlas or local):
```python
client = MongoClient("your-mongodb-uri")
```

Alternatively, use environment variables for `MONGO_URI` for production.

---

## 🚀 Running the server

**Development (with reload):**
```bash
uvicorn main:app --reload
```

**Production (e.g., on Railway):**
```bash
uvicorn main:app --host 0.0.0.0 --port ${PORT}
```

The API will be available at:
```
http://localhost:8000
```

---

## 📌 API Endpoints

### ➡️ Create Product
**POST** `/products`  
Request body:
```json
{
  "name": "Shirt",
  "price": 20.00,
  "sizes": {
    "size": "10",
    "quantity": 5
  }
}
```
Response:
```json
{
    "id": "1234567890"
}
```

---

### ➡️ List Products
**GET** `/products`  
Query params (all optional):
- `name` → partial/regex search
- `size` → filter by size
- `limit` → number of docs (default 10)
- `offset` → number of docs to skip

Response:
```json
{
  "data": [
    {
      "id": 12345,
      "name": "T-Shirt",
      "price": 19
    },
    {
      "id": 12346,
      "name": "Shirt",
      "price": 20
    }
  ],
  "page": {
    "next": null,
    "limit": 10,
    "previous": null
  }
}
```

---

### ➡️ Create Order
**POST** `/orders`  
Request body:
```json
{
  "userId": "user_1",
  "items": [
    {
      "productId": "12345",
      "qty": 3
    },
    {
      "productId": "12346",
      "qty": 5
    }
  ]
}

```
Response:
```json
{
  "id": "1234567890"
}
```

---

### ➡️ Get Orders for User
**GET** `/orders/{user_id}`  
Query params:
- `limit`
- `offset`

Response:
```json
{
  "data": [
    {
      "id": "687e702c3acbdf77a9103ec4",
      "item": [
        {
          "productdetails": {
            "name": "T-Shirt",
            "id": "12345"
          },
          "qty": 3
        },
        {
          "productdetails": {
            "name": "Shirt",
            "id": "12346"
          },
          "qty": 5
        }
      ],
      "total": 157
    }
  ],
  "page": {
    "next": null,
    "limit": 10,
    "previous": null
  }
}
```

---

## 🌐 Deployment on Railway

✅ Add your `MONGO_URI` in Railway **Environment Variables**.  
✅ Set the start command in Railway:
```
uvicorn main:app --host 0.0.0.0 --port ${PORT}
```

---

## 📁 Project Structure

```
.
├── main.py          # FastAPI endpoints
├── db.py            # MongoDB connection & helpers
├── requirements.txt # dependencies
└── README.md        # this file
```

