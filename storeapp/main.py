from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel
from fastapi.middleware.cors import CORSMiddleware
import requests


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)

redis = get_redis_connection(
    host="redis-11506.c55.eu-central-1-1.ec2.cloud.redislabs.com",
    port="11506",
    password="0N7WLgT69T9YIHCTtlL8X8jDV179UF3X",
    decode_responses=True
)


class ProductOrder(HashModel):
    product_id:str
    quantity:str
    class Meta:
        database=redis


class Order(HashModel):
    product_id:str
    price:float
    total:float
    quantity:int
    status:str
    class Meta:
        database=redis


@app.post("/orders")
def create(productOrder:ProductOrder):
    pass
    # req = re