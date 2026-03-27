from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.marketing import Coupon, Campaign, NewsletterSubscriber
from app.schema.marketing import (
    CouponCreate, CouponUpdate, CouponOut,
    CampaignCreate, CampaignUpdate, CampaignOut,
    SubscriberCreate, SubscriberOut
)

router = APIRouter(prefix="/marketing", tags=["Marketing & Promotions"])

# ---------------- Coupons ----------------
@router.post("/coupons", response_model=CouponOut)
def create_coupon(coupon: CouponCreate, db: Session = Depends(get_db)):
    new_coupon = Coupon(**coupon.model_dump())
    db.add(new_coupon)
    db.commit()
    db.refresh(new_coupon)
    return new_coupon

@router.get("/coupons", response_model=list[CouponOut])
def list_coupons(db: Session = Depends(get_db)):
    return db.query(Coupon).all()

@router.put("/coupons/{coupon_id}", response_model=CouponOut)
def update_coupon(coupon_id: int, update: CouponUpdate, db: Session = Depends(get_db)):
    record = db.query(Coupon).filter(Coupon.coupon_id == coupon_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Coupon not found")
    for key, value in update.model_dump(exclude_unset=True).items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record

@router.delete("/coupons/{coupon_id}")
def delete_coupon(coupon_id: int, db: Session = Depends(get_db)):
    record = db.query(Coupon).filter(Coupon.coupon_id == coupon_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Coupon not found")
    db.delete(record)
    db.commit()
    return {"message": "Coupon deleted successfully"}


# ---------------- Campaigns ----------------
@router.post("/campaigns", response_model=CampaignOut)
def create_campaign(campaign: CampaignCreate, db: Session = Depends(get_db)):
    new_campaign = Campaign(**campaign.model_dump())
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)
    return new_campaign

@router.get("/campaigns", response_model=list[CampaignOut])
def list_campaigns(db: Session = Depends(get_db)):
    return db.query(Campaign).all()

@router.put("/campaigns/{campaign_id}", response_model=CampaignOut)
def update_campaign(campaign_id: int, update: CampaignUpdate, db: Session = Depends(get_db)):
    record = db.query(Campaign).filter(Campaign.campaign_id == campaign_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Campaign not found")
    for key, value in update.model_dump(exclude_unset=True).items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record

@router.delete("/campaigns/{campaign_id}")
def delete_campaign(campaign_id: int, db: Session = Depends(get_db)):
    record = db.query(Campaign).filter(Campaign.campaign_id == campaign_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Campaign not found")
    db.delete(record)
    db.commit()
    return {"message": "Campaign deleted successfully"}


# ---------------- Newsletter Subscribers ----------------
@router.post("/subscribers", response_model=SubscriberOut)
def add_subscriber(subscriber: SubscriberCreate, db: Session = Depends(get_db)):
    new_subscriber = NewsletterSubscriber(**subscriber.model_dump())
    db.add(new_subscriber)
    db.commit()
    db.refresh(new_subscriber)
    return new_subscriber

@router.get("/subscribers", response_model=list[SubscriberOut])
def list_subscribers(db: Session = Depends(get_db)):
    return db.query(NewsletterSubscriber).all()

@router.delete("/subscribers/{subscriber_id}")
def delete_subscriber(subscriber_id: int, db: Session = Depends(get_db)):
    record = db.query(NewsletterSubscriber).filter(NewsletterSubscriber.subscriber_id == subscriber_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    db.delete(record)
    db.commit()
    return {"message": "Subscriber deleted successfully"}
# ---------------- End of Marketing & Promotions Routes ----------------

# dashboard route for marketing overview
@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):    
    return {
        "total_coupons": db.query(Coupon).count(),
        "total_campaigns": db.query(Campaign).count(),
        "total_subscribers": db.query(NewsletterSubscriber).count()
    }   