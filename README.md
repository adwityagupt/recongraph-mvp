
# ReconGraph DocReconcile — MVP (Cost-free)

**What it does**
- Upload two files (e.g., Bank Statement CSV + Ledger CSV)
- Auto-match rows (amount/date/ref/party with fuzzy matching)
- Show matches + exceptions
- Generate **Bank Reconciliation Statement (PDF)** or **Generic Reconciliation Certificate (PDF)**
- Export matches to CSV

**Stack (free)**
- UI: Streamlit (free hosting on streamlit.io)
- Matching: pandas + rapidfuzz (optional)
- Certificates: reportlab (PDF)
- Storage: not required (runs in-session). You can add Drive/Firebase later.

## Run locally
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```
Open the URL shown by Streamlit in your browser.

## Deploy free on Streamlit Cloud
1. Push this folder to a new **public GitHub repo**.
2. Go to https://share.streamlit.io → “New app” → connect your repo.
3. Main file: `streamlit_app.py` ; Python version: 3.10+
4. Add `requirements.txt`. Deploy.

## Extend to GST / VAT / FIRC
- GST 2A/2B JSON → convert to CSV via small script; then use app.
- VAT (Saudi/EU) → export tax portal data → load + reconcile with ERP.
- FIRC → add PDF parser & invoice linking (Phase 2).

## Notes
- PDF bank parsing varies; MVP expects CSV/XLSX uploads.
- Ask banks/PGs for CSV export (commonly available).
