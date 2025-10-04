from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
from io import BytesIO

def _canvas_bytes(draw_fn):
    """Create an in-memory PDF and return raw bytes."""
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    draw_fn(c)
    c.showPage()
    c.save()
    buf.seek(0)
    return buf.getvalue()

def generate_bank_reco_pdf_bytes(company_name, period, matches_count, left_unmatched, right_unmatched):
    def _draw(c):
        w, h = A4
        y = h - 60
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, "Bank Reconciliation Statement")
        y -= 25
        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"Company: {company_name}")
        y -= 18
        c.drawString(50, y, f"Period: {period}")
        y -= 18
        c.drawString(50, y, f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
        y -= 30
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Summary")
        y -= 18
        c.setFont("Helvetica", 12)
        c.drawString(65, y, f"Matched entries: {matches_count}")
        y -= 16
        c.drawString(65, y, f"Unmatched (Bank): {left_unmatched}")
        y -= 16
        c.drawString(65, y, f"Unmatched (Books): {right_unmatched}")
        y -= 40
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(50, y, "Note: System-generated summary. Attach detailed schedules for audit/CA use.")
    return _canvas_bytes(_draw)

def generate_generic_cert_pdf_bytes(title, company_name, period, notes=""):
    def _draw(c):
        w, h = A4
        y = h - 60
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, title)
        y -= 25
        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"Company: {company_name}")
        y -= 18
        c.drawString(50, y, f"Period: {period}")
        y -= 18
        if notes:
            c.drawString(50, y, f"Notes: {notes}")
            y -= 18
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(50, y, "This is a system-generated document; CA sign-off may be required.")
    return _canvas_bytes(_draw)
