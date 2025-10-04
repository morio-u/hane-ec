from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import home, products, auth, users, cart, checkout
from app.core.exceptions import RedirectHomeException
from app.core.exception_handlers import redirect_home_handler

app = FastAPI()
app.add_exception_handler(RedirectHomeException, redirect_home_handler)

# shop
app.mount("/static", StaticFiles(directory="app/static/shop"), name="static")
app.include_router(home.router)
app.include_router(products.router)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(cart.router, prefix="/cart", tags=["cart"])
app.include_router(checkout.router, prefix="/checkout", tags=["checkout"])
