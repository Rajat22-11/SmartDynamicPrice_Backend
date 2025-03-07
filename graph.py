from fastapi import FastAPI, Query
import pandas as pd
import plotly.express as px
import io
from fastapi.responses import HTMLResponse

# Initialize FastAPI
app = FastAPI()

class StockTrendAPI:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = self.load_data()

    def load_data(self):
        """Loads and preprocesses the CSV data"""
        try:
            df = pd.read_csv(self.data_path)
            required_columns = {"Order Year", "Order Month", "Order Day", "Location", "Product Name", "Max Stock"}
            
            if not required_columns.issubset(df.columns):
                return None  # Return None if required columns are missing

            df["Order Date"] = pd.to_datetime(
                df["Order Year"].astype(str) + "-" +
                df["Order Month"].astype(str) + "-" +
                df["Order Day"].astype(str)
            )
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return None  # Return None if loading fails

    def get_stock_trend(self, location: str, product: str):
        """Generates an HTML plot showing stock trends over time"""
        if self.df is None:
            return HTMLResponse(content="<h3>Data failed to load. Please check your CSV file.</h3>", status_code=500)

        df_location = self.df[
            (self.df["Location"] == location) & (self.df["Product Name"] == product)
        ]

        if df_location.empty:
            return HTMLResponse(content=f"<h3>No data found for {product} in {location}</h3>", status_code=404)

        time_series_data = df_location.groupby("Order Date")["Max Stock"].sum().reset_index()

        fig = px.line(
            time_series_data,
            x="Order Date",
            y="Max Stock",
            title=f"Stock Level Trend Over Time in {location} for {product}",
            labels={"Order Date": "Date", "Max Stock": "Stock Level"},
            template="plotly_dark",
        )

        html_buffer = io.StringIO()
        fig.write_html(html_buffer)

        return HTMLResponse(content=html_buffer.getvalue(), status_code=200)