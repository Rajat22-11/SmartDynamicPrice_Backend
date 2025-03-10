from fastapi import FastAPI, Query
import pandas as pd
import plotly.express as px
import io
from fastapi.responses import HTMLResponse


class StockTrendAPI:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = self.load_data()

    def load_data(self):
        df = pd.read_csv(self.data_path)
        year_col = df.get("Order Year")
        month_col = df.get("Order Month")
        day_col = df.get("Order Day")

        if year_col is not None and month_col is not None and day_col is not None:
            df["Order Date"] = pd.to_datetime(
                year_col.astype(str)
                + "-"
                + month_col.astype(str)
                + "-"
                + day_col.astype(str)
            )
        else:
            raise ValueError("Some required columns are missing!")

        return df

    def get_stock_trend(self, location: str, product: str):
        df_location = self.df[
            (self.df["Location"] == location) & (self.df["Product Name"] == product)
        ]
        time_series_data = (
            df_location.groupby("Order Date")["Max Stock"].sum().reset_index()
        )

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
        return HTMLResponse(content=html_buffer.getvalue())
