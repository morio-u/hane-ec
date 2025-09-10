from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import home, products, auth, users

app = FastAPI()

# shop
app.mount("/static", StaticFiles(directory="app/static/shop"), name="static")
app.include_router(home.router)
app.include_router(products.router)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])