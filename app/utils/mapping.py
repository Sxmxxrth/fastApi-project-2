# app/utils/mapping.py
from app.models.order import Order
from app.schema.invoice import InvoiceCreate, InvoiceItemCreate

def map_order_to_invoice(order: Order) -> InvoiceCreate:
    invoice_items = [
        InvoiceItemCreate(
            description=item.product.name,   # use Product relationship
            qty=item.quantity,
            unit_price=float(item.price),
            tax=0.0
        )
        for item in order.order_items
    ]
    return InvoiceCreate(
        user_name=order.user_name,
        status="pending",
        items=invoice_items
    )
