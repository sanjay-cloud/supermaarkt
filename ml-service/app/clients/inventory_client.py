from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

def check_inventory(id : str):
    
    inventory_url = f"{os.getenv('INVENTORY_API_BASE_URL')}/api/v1/inventory/{id}"
    return requests.get(inventory_url).json()