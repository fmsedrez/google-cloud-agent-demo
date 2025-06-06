from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/city/{city_name}")
async def read_item(city_name: str, q: str = None):
    weather_data = {
        "New York": "Sunny, 25°C",
        "London": "Cloudy, 18°C",
        "Tokyo": "Rainy, 22°C",
        "Campo Mourao": "Sunny, 25°C",
        "Cascavel": "Sunny, 25°C",
        "Curitiba": "Rainy, 25°C",
        "Sao Paulo": "Sunny, 25°C",
        "Rio de Janeiro": "Sunny, 25°C",
        "Belo Horizonte": "Sunny, 25°C",
        "Brasilia": "Sunny, 25°C",
        "Salvador": "Sunny, 25°C",
        "Pelotas": "Cloudy, 25°C",
        "Porto Alegre": "Sunny, 25°C",
        "Porto Velho": "Rainy, 25°C",
        "Rio Branco": "Sunny, 25°C",
        "Manaus": "Cloudy, 25°C",
        "Boa Vista": "Sunny, 25°C",
        "Macapa": "Sunny, 25°C",
    }
    return weather_data.get(city_name, "Weather data not available.")
