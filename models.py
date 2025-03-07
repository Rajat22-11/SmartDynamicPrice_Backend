from pydantic import BaseModel, Field
from typing import Annotated

# Define input schema with date validation
class DiscountPredictionInput(BaseModel):
    Product_Name: str
    Category: str
    Location: str
    MRP: float
    Blinkit_Price: float
    Zepto_Price: float
    Instamart_Price: float
    Margin: float
    Festive_Seasonal_Impact: str
    Shelf_Life_days: float
    Min_Stock: float
    Max_Stock: float
    Customer_Sentiment: str
    Weight_g: float
    Weight_Unit: str
    Order_Date: Annotated[str, Field(pattern=r"\d{4}-\d{2}-\d{2}")]  # Ensures YYYY-MM-DD format
    Order_Hour: int  # Extract Order_Time_Category dynamically
    customer_type: str
