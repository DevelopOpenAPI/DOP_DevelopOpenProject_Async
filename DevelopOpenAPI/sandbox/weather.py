import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

class param1(BaseModel):
    url: str
    cityId: str


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.post("/apitest")
async def weather_get(param: param1):
    city = {'city': param.cityId}
    url = param.url
    response = requests.get(url, params=city)
    return (response.text)

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8080)