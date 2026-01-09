from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings
from app.routers.shop import home, products, auth, users, cart, checkout
from app.routers.admin import auth as admin_auth, dashboard, products as admin_products
from app.core.exception import RedirectHomeException
from app.core.exception_handler import (
    shop_redirect_home_handler,
    admin_validation_exception_handler,
)

app = FastAPI()
app.add_exception_handler(RedirectHomeException, shop_redirect_home_handler)
app.add_exception_handler(RequestValidationError, admin_validation_exception_handler)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# common
app.mount(
    "/static/uploads", StaticFiles(directory="app/static/uploads"), name="uploads"
)

# shop
app.mount("/static/shop", StaticFiles(directory="app/static/shop"), name="static")
app.include_router(home.router)
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(cart.router, prefix="/cart", tags=["cart"])
app.include_router(checkout.router, prefix="/checkout", tags=["checkout"])

# admin
app.mount(
    "/static/admin", StaticFiles(directory="app/static/admin"), name="admin_static"
)
app.include_router(admin_auth.router, prefix="/admin/auth", tags=["auth"])
app.include_router(dashboard.router, prefix="/admin", tags=["admin"])
app.include_router(admin_products.router, prefix="/admin/products", tags=["products"])
