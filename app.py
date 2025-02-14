import streamlit as st
import streamlit_qrcode_scanner as qrcode_scanner
import pandas as pd
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import qrcode
import io
from PIL import Image

st.header("Beställ dessa varor")

uri = "mongodb+srv://maxroupe00:RmNRuycytbFS73bi@maxroupe.nqqba.mongodb.net/?retryWrites=true&w=majority&appName=MaxRoupe"

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

databse = client["northwind"]

collection = databse["product_suppliers"]

product_df = pd.read_csv(r"C:\Users\maxro\Documents\Skola\DM24H\Databastyper\Kunskapskontroll1\data\northwind\products.csv")

file_path = r"C:\Users\maxro\Documents\Skola\DM24H\Databastyper\Kunskapskontroll1\data\northwind\suppliers.json"

with open(file_path, "r", encoding="utf-8") as f:
    suppliers_data = json.load(f)

suppliers_df = pd.DataFrame(suppliers_data)

merged_df = product_df.merge(suppliers_df, on="SupplierID", how="left")

merged_data = merged_df.to_dict(orient="records")

collection.delete_many({})

collection.insert_many(merged_data)

query = {
    "$expr": {
        "$gt": ["$ReorderLevel", {"$sum": ["$UnitsInStock", "$UnitsOnOrder"]}]
    }
}

products_to_order = collection.find(query, {"ProductID": 1, "ProductName": 1, "CompanyName": 1, "ContactName": 1, "Phone": 1, "ReorderLevel": 1, "UnitsInStock": 1, "UnitsOnOrder": 1})

for product in products_to_order:
    st.subheader(f"{product['ProductName']}")
    st.write(f"***Product ID:*** {product["ProductID"]}")
    st.write(f"***Företag:*** {product["CompanyName"]}")
    st.write(f"***Kontakt person:*** {product["ContactName"]}")
    st.write(f"***Telefon:*** {product["Phone"]}")
    st.write(f"***Beställningsnivå:*** {product["ReorderLevel"]}")
    st.write(f"***Produkter påväg:*** {product["UnitsOnOrder"]}")
    st.write(f"***Produkter i lager:*** {product["UnitsInStock"]}")
    st.divider()