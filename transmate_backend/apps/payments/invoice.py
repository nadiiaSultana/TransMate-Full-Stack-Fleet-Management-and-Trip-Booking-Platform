from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def generate_invoice_pdf(payment):
    buffer=BytesIO(); pdf=canvas.Canvas(buffer,pagesize=A4); width,height=A4; y=height-60
    pdf.setFont('Helvetica-Bold',20); pdf.drawString(50,y,'TransMate Payment Invoice'); y-=40
    pdf.setFont('Helvetica',11)
    lines=[f'Invoice ID: TM-INV-{payment.id}',f'Payment Status: {payment.status}',f'Payment Method: {payment.payment_method}',f'Transaction ID: {payment.transaction_id or "N/A"}','', 'Customer Information', f'Name: {payment.customer.username}', f'Email: {payment.customer.email}', f'Phone: {payment.customer.phone or "N/A"}', '', 'Trip Information', f'Booking ID: {payment.booking.id}', f'Pickup: {payment.booking.pickup_location}', f'Drop-off: {payment.booking.dropoff_location}', f'Distance: {payment.booking.distance_km} KM', '', f'Total Amount: BDT {payment.amount}', '', 'Thank you for using TransMate.']
    for line in lines:
        if line in ['Customer Information','Trip Information'] or line.startswith('Total Amount'):
            pdf.setFont('Helvetica-Bold',13)
        else: pdf.setFont('Helvetica',11)
        pdf.drawString(50,y,line[:95]); y-=22
    pdf.showPage(); pdf.save(); buffer.seek(0); return buffer
