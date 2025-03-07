import pickle
import pandas as pd
from datetime import datetime

# Load the trained model
with open("trained_model.pkl", "rb") as f:
    model = pickle.load(f)

# Load the saved scaler
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# Load the saved label encoders
with open("label_encoders.pkl", "rb") as f:
    label_encoders = pickle.load(f)

# Load the saved label encoder for 'Order_Time_Category'
with open("le_time.pkl", "rb") as f:
    le_time = pickle.load(f)

# Function to determine Order_Time_Category based on Order_Hour
def get_order_time_category(hour: int) -> str:
    if 5 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 21:
        return "Evening"
    else:
        return "Night"

# Function to preprocess input data
def preprocess_input(input_dict):
    # Extract year, month, and day from Order_Date
    order_date = datetime.strptime(input_dict["Order_Date"], "%Y-%m-%d")
    input_dict["Order_Year"] = order_date.year
    input_dict["Order_Month"] = order_date.month
    input_dict["Order_Day"] = order_date.day

    # Determine Order_Time_Category dynamically
    input_dict["Order_Time_Category"] = get_order_time_category(input_dict["Order_Hour"])

    # Remove Order_Date (not needed for ML model)
    del input_dict["Order_Date"]

    # Convert dictionary to DataFrame
    df = pd.DataFrame([input_dict])

    # Apply label encoding to categorical columns
    categorical_columns = ["Category", "Location", "Festive_Seasonal_Impact", 
                           "Customer_Sentiment", "Product_Name", "Weight_Unit"]

    for col in categorical_columns:
        if col in label_encoders:
            if input_dict[col] in label_encoders[col].classes_:
                df[col] = label_encoders[col].transform([input_dict[col]])[0]
            else:
                df[col] = 0  # Handle unseen categories safely

    # Encode 'Order_Time_Category'
    if input_dict["Order_Time_Category"] in le_time.classes_:
        df["Order_Time_Category"] = le_time.transform([input_dict["Order_Time_Category"]])[0]
    else:
        df["Order_Time_Category"] = 0  # Handle unseen time categories

    # Select numerical columns and apply MinMaxScaler
    numerical_columns = ["MRP", "Blinkit_Price", "Zepto_Price", "Instamart_Price", "Margin",
                         "Shelf_Life_days", "Min_Stock", "Max_Stock", 
                         "Order_Year", "Order_Month", "Order_Day", "Order_Hour", "Weight_g"]

    df[numerical_columns] = scaler.transform(df[numerical_columns])

    # Ensure column order matches the trained model
    expected_columns = model.get_booster().feature_names
    df = df[expected_columns]  # Reorder columns

    return df
