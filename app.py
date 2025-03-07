import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from database import SupabaseService
from models import DiscountPredictionInput
from utils import preprocess_input, model
from graph import StockTrendAPI


load_dotenv()


db = SupabaseService()

app = FastAPI(title="Price Flow")


origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:5173",
    "http://localhost:5174",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Welcome to Smart Dynamic Pricing System"}


@app.get("/product/{product_name}")
def get_product(product_name: str):
    return db.get_product_detail(product_name)


@app.get("/categories")
def get_categories():
    return db.get_unique_categories()


@app.get("/products/{category_name}")
def get_products(category_name: str):
    return db.get_products_by_category(category_name)


@app.post("/predict_discount/")
def predict_discount(input_data: DiscountPredictionInput):
    input_dict = input_data.dict()
    df = preprocess_input(input_dict)
    prediction = model.predict(df)

    max_discount = float(prediction[0])
    customer_type = input_dict["customer_type"].lower()

    if customer_type == "premium":
        discount = 0.75 * max_discount
    elif customer_type == "normal":
        discount = 0.45 * max_discount
    else:
        discount = 0.25 * max_discount

    return {"max_discount": discount}


base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "synthetic_dataset1.csv")

if not os.path.exists(file_path):
    raise FileNotFoundError(f"Error: File not found at {file_path}")

stock_trend_api = StockTrendAPI(file_path)


@app.get("/stock_trend", response_class=HTMLResponse)
async def stock_trend(
    location: str = Query(..., description="Store location"),
    product: str = Query(..., description="Product name"),
):
    graph = stock_trend_api.get_stock_trend(location, product)
    return {"graph": graph}


# Start the application with dynamic port for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  #
    uvicorn.run(app, host="0.0.0.0", port=port)
