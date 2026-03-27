from fastapi import APIRouter
from .auth import router as auth_router
from .categories import router as categories
from .orders import router as orders
from .employees import router as employees
from .tasks import router as tasks
from .posts import router as posts
from .roles import router as roles
from .products import router as products
from .reviews import router as reviews
from .users import router as users
from .attendence import router as attendence
from .carts import router as carts
from .favorites import router as favorites
from .system_log import router as system_log
from .admin import router as admin
from .payment import router as payment
from .salary import router as salary
from .order_item import router as order_item
from .security_ac import router as security_ac
from .inventory import router as inventory
from .shipping import router as shipping
from .analytics import router as analytics
from .fraud import router as fraud
from .invoice import router as invoice
from .marketing import router as marketing
from .audit_trail import router as audit_trail

all_routers = [
    categories,
    orders,
    employees,
    tasks,
    posts,
    roles,
    products,
    reviews,
    users,
    attendence,
    carts,
    favorites,
    system_log,
    admin,
    payment,
    salary,
    order_item,
    security_ac,
    inventory,
    shipping,
    analytics,
    fraud,
    invoice,
    marketing,
    audit_trail
]


router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["auth"])
