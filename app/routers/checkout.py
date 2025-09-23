from datetime import datetime
from fastapi import Request, APIRouter, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.order import Order

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/shop")


@router.post("", response_class=HTMLResponse)
def view_checkout_form(
    request: Request, subtotal_amount: float = Form(...), user=Depends(get_current_user)
):
    return templates.TemplateResponse(
        "checkout_form.html",
        {"request": request, "user": user, "subtotal_amount": subtotal_amount},
    )


@router.post("/confirm", response_class=HTMLResponse)
async def checkout_confirm(
    request: Request,
    shipping_last_name: str = Form(...),
    shipping_first_name: str = Form(...),
    shipping_address_line1: str = Form(...),
    shipping_address_line2: str = Form(""),
    shipping_city: str = Form(...),
    shipping_state: str = Form(...),
    shipping_zip: str = Form(...),
    shipping_phone_number: str = Form(...),
    shipping_method: str = Form(...),
    subtotal_amount: float = Form(...),
    payment_method: str = Form(...),
    card_number: str = Form(...),
    card_name: str = Form(...),
    card_cvv: str = Form(...),
    user=Depends(get_current_user),
):
    # TODO: Add validation
    order_data = {
        "shipping_last_name": shipping_last_name,
        "shipping_first_name": shipping_first_name,
        "shipping_address_line1": shipping_address_line1,
        "shipping_address_line2": shipping_address_line2,
        "shipping_city": shipping_city,
        "shipping_state": shipping_state,
        "shipping_zip": shipping_zip,
        "shipping_phone_number": shipping_phone_number,
        "shipping_method": shipping_method,
        "subtotal_amount": subtotal_amount,
        "payment_method": payment_method,
        "card_number": card_number,
        "card_name": card_name,
        "card_cvv": card_cvv,
    }
    return templates.TemplateResponse(
        "checkout_confirm.html", {"request": request, "order": order_data, "user": user}
    )


@router.post("/complete", name="checkout_complete", response_class=HTMLResponse)
def checkout_complete(
    request: Request,
    db: Session = Depends(get_db),
    shipping_last_name: str = Form(...),
    shipping_first_name: str = Form(...),
    shipping_address_line1: str = Form(...),
    shipping_address_line2: str = Form(""),
    shipping_city: str = Form(...),
    shipping_state: str = Form(...),
    shipping_zip: str = Form(...),
    shipping_phone_number: str = Form(...),
    shipping_method: str = Form(...),
    payment_method: str = Form(...),
    card_number: str = Form(...),
    card_name: str = Form(...),
    card_cvv: str = Form(...),
    subtotal_amount: float = Form(...),
    user=Depends(get_current_user),
):
    """
    1. フォームデータ受け取り
    2. orders, order_items, payments に保存
    3. 完了画面を表示
    """

    # ---- 注文データ保存（簡易版） ----
    new_order = Order(
        user,  # ゲスト購入なら None、会員ならユーザーIDをセット
        last_name,
        first_name,
        address_line1,
        address_line2,
        city,
        state,
        zip,
        shipping_address=f"{state} {city} {address_line1} {address_line2}",
        shipping_method=shipping_method,
        status="pending",
        order_date=datetime.now(),
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # TODO: カート情報を order_items に保存
    # 今は仮で 1 商品だけ保存
    order_item = OrderItem(
        order_id=new_order.id, product_id=1, quantity=1, price=1000  # 仮
    )
    db.add(order_item)

    # 決済情報
    payment = Payment(
        order_id=new_order.id, amount=1000, method=payment_method, status="authorized"
    )
    db.add(payment)

    db.commit()

    return templates.TemplateResponse(
        "checkout_complete.html", {"request": request, "order": new_order}
    )
