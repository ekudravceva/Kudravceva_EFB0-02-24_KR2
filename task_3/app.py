from fastapi import FastAPI, status
from models import UserCreate

app = FastAPI(
    title="Task 3 API",
)

sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}

sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]

@app.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    return user

@app.get("/products/search")
async def search_products(keyword: str, category: str = None, limit: int = 10):
    result = []
    for product in sample_products:
        if keyword.lower() in product["name"].lower():
            result.append(product)

    if category:
        result = [p for p in result if p["category"].lower() == category.lower()]
    
    result = result[:limit]
    
    return result

@app.get("/product/{product_id}")
async def get_product(product_id: int):
    for product in sample_products:
        if product["product_id"] == product_id:
            return product
    
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Product not found")