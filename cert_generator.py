from fpdf import FPDF
from datetime import datetime

def _pdf_bytes(build_fn):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    build_fn(pdf)
    return bytes(pdf.output(dest="S").encode("latin1"))

def generate_bank_reco_pdf_bytes(company_name, period, matches_count, left_unmatched, right_unmatched):
    def _build(pdf):
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Bank Reconciliation Statement", ln=1)
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 8, f"Company: {company_name}", ln=1)
        pdf.cell(0, 8, f"Period: {period}", ln=1)
        pdf.cell(0, 8, f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", ln=1)
        pdf.ln(4)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "Summary", ln=1)
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 8, f"Matched entries: {matches_count}", ln=1)
        pdf.cell(0, 8, f"Unmatched (Bank): {left_unmatched}", ln=1)
        pdf.cell(0, 8, f"Unmatched (Books): {right_unmatched}", ln=1)
        pdf.ln(6)
        pdf.set_font("Arial", "I", 10)
        pdf.multi_cell(0, 6, "Note: System-generated summary. Attach detailed schedules for audit/CA use.")
    return _pdf_bytes(_build)

def generate_generic_cert_pdf_bytes(title, company_name, period, notes=""):
    def _build(pdf):
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, title, ln=1)
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 8, f"Company: {company_name}", ln=1)
        pdf.cell(0, 8, f"Period: {period}", ln=1)
        if notes:
            pdf.ln(2)
            pdf.multi_cell(0, 6, f"Notes: {notes}")
        pdf.ln(6)
        pdf.set_font("Arial", "I", 10)
        pdf.multi_cell(0, 6, "This is a system-generated document; CA sign-off may be required.")
    return _pdf_bytes(_build)
