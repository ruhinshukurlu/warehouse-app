from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
import requests
import time

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
def create(productOrder:ProductOrder, background_task:BackgroundTasks):
    req = requests.get(f"http://127.0.0.1:8000/product/{productOrder.product_id}")
    product = req.json()
    fee = product['price'] * 0.2

    order = Order(
        product_id = productOrder.product_id,
        price = product['price'],
        fee = fee,
        total = product['price'] + fee,
        quantity = productOrder.quantity,
        status='pending'
    )
    order.save()
    background_task.add_task(order_complete, order)
    return order


@app.get('/orders/{pk}')
def get(pk:str):
    return format(pk)


@app.get('/orders')
def get_all():
    return [format(pk) for pk in Order.all_pks()]



def format(pk:str):
    order = Order.get(pk)
    return {
        "id":order.pk,
        "product_id":order.product_id,
        "fee":order.fee,
        "total":order.total,
        "quantity":order.quantity,
        "status":order.status
    }


def order_complete(order:Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()