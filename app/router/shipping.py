from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.shipping import ShippingProvider, Shipment
from app.schema.shipping import (
    ShippingProviderCreate, ShippingProviderUpdate, ShippingProviderOut,
    ShipmentCreate, ShipmentUpdateStatus, ShipmentOut, ShipmentTracking
)
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/shipping", tags=["Shipping & Delivery"])

# Providers of shipping

@router.get("/shipping-providers", response_model=list[ShippingProviderOut])
def list_providers(db: Session = Depends(get_db)):
    try:
        return db.query(ShippingProvider).all()
    except Exception as ex:
        logger.error(f"Error fetching providers: {ex}")
        raise HTTPException(status_code=500, detail=f"Fetching providers failed: {str(ex)}")

@router.post("/shipping-providers", response_model=ShippingProviderOut)
def add_provider(provider: ShippingProviderCreate, db: Session = Depends(get_db)):
    try:
        db_provider = ShippingProvider(**provider.dict())
        db.add(db_provider)
        db.commit()
        db.refresh(db_provider)
        return db_provider
    except Exception as ex:
        db.rollback()
        logger.error(f"Error adding provider: {ex}")
        raise HTTPException(status_code=500, detail=f"Adding provider failed: {str(ex)}")

@router.put("/shipping-providers/{id}", response_model=ShippingProviderOut)
def update_provider(id: int, provider: ShippingProviderUpdate, db: Session = Depends(get_db)):
    try:
        db_provider = db.query(ShippingProvider).filter(ShippingProvider.provider_id == id).first()
        if not db_provider:
            raise HTTPException(status_code=404, detail="Provider not found")
        for key, value in provider.dict(exclude_unset=True).items():
            setattr(db_provider, key, value)
        db.commit()
        db.refresh(db_provider)
        return db_provider
    except Exception as ex:
        db.rollback()
        logger.error(f"Error updating provider {id}: {ex}")
        raise HTTPException(status_code=500, detail=f"Updating provider failed: {str(ex)}")


# Shipments for orders

@router.get("/shipments", response_model=list[ShipmentOut])
def list_shipments(db: Session = Depends(get_db)):
    try:
        return db.query(Shipment).all()
    except Exception as ex:
        logger.error(f"Error fetching shipments: {ex}")
        raise HTTPException(status_code=500, detail=f"Fetching shipments failed: {str(ex)}")

@router.post("/shipments", response_model=ShipmentOut)
def create_shipment(shipment: ShipmentCreate, db: Session = Depends(get_db)):
    try:
        db_shipment = Shipment(**shipment.dict())
        db.add(db_shipment)
        db.commit()
        db.refresh(db_shipment)
        return db_shipment
    except Exception as ex:
        db.rollback()
        logger.error(f"Error creating shipment: {ex}")
        raise HTTPException(status_code=500, detail=f"Creating shipment failed: {str(ex)}")

@router.put("/shipments/{id}/status", response_model=ShipmentOut)
def update_shipment_status(id: int, status_update: ShipmentUpdateStatus, db: Session = Depends(get_db)):
    try:
        db_shipment = db.query(Shipment).filter(Shipment.shipment_id == id).first()
        if not db_shipment:
            raise HTTPException(status_code=404, detail="Shipment not found")
        db_shipment.status = status_update.status
        db.commit()
        db.refresh(db_shipment)
        return db_shipment
    except Exception as ex:
        db.rollback()
        logger.error(f"Error updating shipment {id} status: {ex}")
        raise HTTPException(status_code=500, detail=f"Updating shipment status failed: {str(ex)}")

@router.get("/shipments/{id}/tracking", response_model=ShipmentTracking)
def track_shipment(id: int, db: Session = Depends(get_db)):
    try:
        db_shipment = db.query(Shipment).filter(Shipment.shipment_id == id).first()
        if not db_shipment:
            raise HTTPException(status_code=404, detail="Shipment not found")
        return ShipmentTracking(
            shipment_id=db_shipment.shipment_id,
            tracking_number=db_shipment.tracking_number,
            status=db_shipment.status
        )
    except Exception as ex:
        logger.error(f"Error tracking shipment {id}: {ex}")
        raise HTTPException(status_code=500, detail=f"Tracking shipment failed: {str(ex)}")
