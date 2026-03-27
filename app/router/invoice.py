from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from app.core.database import get_db
from app.schema.invoice import InvoiceCreate, InvoiceOut, InvoiceItemCreate
from app.models.invoice import Invoice, InvoiceItem
from app.models.order import Order
from app.utils.pdf import generate_invoice_pdf
from fastapi.responses import StreamingResponse
from app.utils.mapping import map_order_to_invoice



router = APIRouter(prefix="/invoices", tags=["Invoices"])

@router.post("/", response_model=InvoiceOut)
def create_invoice(invoice_data: InvoiceCreate, db: Session = Depends(get_db)):
    try:
        # Calculate total amount
        total_amount = sum(item.qty * item.unit_price + item.tax for item in invoice_data.items)

        # Create invoice
        invoice = Invoice(
            user_name=invoice_data.user_name,
            status=invoice_data.status,
            total_amount=total_amount,
            amount_paid=0.0
        )
        db.add(invoice)
        db.commit()
        db.refresh(invoice)

        # Create invoice items
        for item_data in invoice_data.items:
            try:
                item_total = item_data.qty * item_data.unit_price + item_data.tax
                item = InvoiceItem(
                    invoice_id=invoice.invoice_id,
                    description=item_data.description,
                    qty=item_data.qty,
                    unit_price=item_data.unit_price,
                    tax=item_data.tax,
                    total=item_total
                )
                db.add(item)
            except Exception as e_item:
                db.rollback()
                raise HTTPException(status_code=500, detail=f"Error creating invoice item: {str(e_item)}")

        db.commit()
        db.refresh(invoice)

        return invoice
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating invoice: {str(e)}")


@router.get("/{invoice_id}", response_model=InvoiceOut)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    try:
        invoice = db.query(Invoice).filter(Invoice.invoice_id == invoice_id).first()
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        return invoice
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching invoice: {str(e)}")


@router.get("/{invoice_id}/pdf")
def get_invoice_pdf(invoice_id: int, db: Session = Depends(get_db)):
    try:
        invoice = (
            db.query(Invoice)
            .filter(Invoice.invoice_id == invoice_id)
            .options(selectinload(Invoice.items))
            .first()
        )
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")

        try:
            pdf_buffer = generate_invoice_pdf(invoice)
            return StreamingResponse(
                pdf_buffer,
                media_type="application/pdf",
                headers={"Content-Disposition": f"attachment; filename=invoice_{invoice.invoice_id}.pdf"}
            )
        except Exception as e_pdf:
            raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e_pdf)}")

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching invoice for PDF: {str(e)}")


# Additional endpoints like update, delete can be added similarly
@router.put("/{invoice_id}", response_model=InvoiceOut)
def update_invoice(invoice_id: int, invoice_data: InvoiceCreate, db: Session = Depends(get_db)):
    try:
        invoice = db.query(Invoice).filter(Invoice.invoice_id == invoice_id).first()
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")

        invoice.user_name = invoice_data.user_name
        invoice.status = invoice_data.status
        invoice.total_amount = sum(item.qty * item.unit_price + item.tax for item in invoice_data.items)
        invoice.amount_paid = 0.0

        db.commit()
        db.refresh(invoice)

        return invoice
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating invoice: {str(e)}")
    
# endpoint to genrate invovice automatically from order can be added here
@router.post("/from_order/{order_id}", response_model=InvoiceOut)
def create_invoice_from_order(order_id: int, db: Session = Depends(get_db)):
    try:
        order = db.query(Order).filter(Order.order_id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        
        invoice_data = map_order_to_invoice(order)

        return create_invoice(invoice_data, db)

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating invoice from order: {str(e)}")


# DASHBOARD ENDPOINTS WHERE ALL INVOICES DETAILS CAN BE FETCHED
@router.get("/", response_model=list[InvoiceOut])
def list_invoices(db: Session = Depends(get_db)):
    try:
        return db.query(Invoice).all()
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error fetching invoices: {ex}")
    

# get invoice pdf from order id
@router.get("/from_order/{order_id}/pdf")
def get_invoice_pdf_from_order(order_id: int, db: Session = Depends(get_db)):
    try:
        order = db.query(Order).filter(Order.order_id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        # Find existing invoice for this order
        invoice = db.query(Invoice).filter(Invoice.order_id == order_id).options(selectinload(Invoice.items)).first()
        if not invoice:
            # If no invoice exists, create one
            invoice_data = map_order_to_invoice(order)
            invoice = create_invoice(invoice_data, db)

        return get_invoice_pdf(invoice.invoice_id, db)

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating/fetching invoice PDF from order: {str(e)}")
