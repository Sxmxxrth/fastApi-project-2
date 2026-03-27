from pydantic import BaseModel

class DashboardSummary(BaseModel):
    users: int
    products: int
    orders: int
    revenue: float


class AdminBase(BaseModel):
    username: str


class AdminCreate(AdminBase):
    password: str


class AdminResponse(AdminBase):
    id: int

    class Config:
        from_attributes = True
        populate_by_name = True  # ✅ correct key for Pydantic v2
