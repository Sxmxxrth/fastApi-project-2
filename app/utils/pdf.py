from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
from app.models.invoice import Invoice

def generate_invoice_pdf(invoice: Invoice) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(name='Title', fontSize=18, alignment=1, spaceAfter=20)
    story.append(Paragraph(f"Invoice #{invoice.invoice_id}", title_style))
    story.append(Spacer(1, 12))

    # Invoice details
    story.append(Paragraph(f"User: {invoice.user_name}", styles['Normal']))   # ✅ fixed
    story.append(Paragraph(f"Status: {invoice.status}", styles['Normal']))
    story.append(Paragraph(f"Total Amount: ${invoice.total_amount:.2f}", styles['Normal']))
    story.append(Paragraph(f"Amount Paid: ${invoice.amount_paid:.2f}", styles['Normal']))
    story.append(Paragraph(f"Created At: {invoice.created_at.strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 12))

    # Items table
    data = [['Description', 'Qty', 'Unit Price', 'Tax', 'Total']]
    for item in invoice.items:
        data.append([
            item.description,
            str(item.qty),
            f"${float(item.unit_price):.2f}",
            f"${float(item.tax):.2f}",
            f"${float(item.total):.2f}"
        ])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(table)

    doc.build(story)
    buffer.seek(0)
    return buffer
