from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import json
load_dotenv()


class SupabaseService:
    def __init__(self):
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        if not supabase_url or not supabase_key:
            raise ValueError("Supabase URL or Key is missing in environment variables")
        self.supabase: Client = create_client(supabase_url, supabase_key)
    
    def get_product_detail(self, product_name):
        try:
            data = self.supabase.table("products").select("*").eq("product_name", product_name).execute()
            product_info = data.json()
            json_data = json.loads(product_info)
            if not json_data['data']:
                raise HTTPException(status_code=404, detail="Product not found")
            return json_data['data'][0]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def get_unique_categories(self):
        try:
            response = self.supabase.table("products").select("product_category").execute()
            categories = list(set(item["product_category"] for item in response.data))
            return {'categories': categories}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def get_products_by_category(self, category_name):
        try:
            response = self.supabase.table("products").select("product_name").eq("product_category", category_name).execute()
            product_names = [item["product_name"] for item in response.data]
            if not product_names:
                raise HTTPException(status_code=404, detail="No products found for this category")
            return {'product_names': product_names}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))