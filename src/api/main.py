from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/stock/{item_name}")
async def read_stock(item_name: str):
    stock_data = {
        "apple": 50,
        "banana": 30,
        "orange": 20,
        "potato": 100,
        "tomato": 200,
        "onion": 320,
        "garlic": 1200,
        "pepper": 500,
        "carrot": 600,
        "lettuce": 700,
    }
    quantity = stock_data.get(item_name)
    if quantity is not None:
        return {"item": item_name, "quantity": quantity}
    else:
        return {"error": "Item not found in stock."}


# Use a sua criatividade para uma nova rota
