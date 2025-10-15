from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings
from app.routers.shop import home, products, auth, users, cart, checkout
from app.routers.admin import dashboard, auth as admin_auth
from app.core.exception import RedirectHomeException
from app.core.exception_handler import redirect_home_handler

app = FastAPI()
app.add_exception_handler(RedirectHomeException, redirect_home_handler)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# shop
app.mount("/static", StaticFiles(directory="app/static/shop"), name="static")
app.include_router(home.router)
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(cart.router, prefix="/cart", tags=["cart"])
app.include_router(checkout.router, prefix="/checkout", tags=["checkout"])

# admin
app.mount(
    "/admin/static", StaticFiles(directory="app/static/admin"), name="admin_static"
)
app.include_router(admin_auth.router, prefix="/admin/auth", tags=["auth"])
app.include_router(dashboard.router, prefix="/admin", tags=["admin"])
