
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_bank_reco_pdf(path_or_buffer, company_name, period, matches_count, left_unmatched, right_unmatched):
    c = canvas.Canvas(path_or_buffer, pagesize=A4)
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
    c.showPage()
    c.save()

def generate_generic_cert_pdf(path_or_buffer, title, company_name, period, notes=""):
    c = canvas.Canvas(path_or_buffer, pagesize=A4)
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
    c.showPage()
    c.save()
