from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import products

app = FastAPI()

# static
app.mount("/static", StaticFiles(directory="app/static/shop"), name="static")

app.include_router(products.router)