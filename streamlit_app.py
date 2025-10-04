
import streamlit as st
import pandas as pd
from io import BytesIO
from recon_engine import load_table, reconcile
from cert_generator import (
    generate_bank_reco_pdf_bytes,
    generate_generic_cert_pdf_bytes
)

st.set_page_config(page_title="ReconGraph DocReconcile MVP", layout="wide")

st.title("ReconGraph — Doc-based AI Reconciliation & Certificates (MVP)")
st.caption("Upload documents → Auto-match → Generate certificate/report (Bank Reco, GST, Turnover, etc.)")

with st.expander("1) Choose Use Case"):
    use_case = st.selectbox("Use case", [
        "Bank Statement vs Books (BRS)",
        "GST 2A/2B vs Books (Summary)",
        "Loan Turnover Certificate (Summary)",
        "Custom Reconciliation"
    ])

st.markdown("---")
st.subheader("2) Upload Documents")
col1, col2 = st.columns(2)

with col1:
    left_file = st.file_uploader("Left table (e.g., Bank Statement CSV/XLSX)", type=["csv","xlsx"])
    left_amount = st.text_input("Left: Amount column", value="amount")
    left_date = st.text_input("Left: Date column", value="date")
    left_ref = st.text_input("Left: Ref/Txn ID column (optional)", value="ref")
    left_party = st.text_input("Left: Party column (optional)", value="party")

with col2:
    right_file = st.file_uploader("Right table (e.g., Books/Ledger CSV/XLSX)", type=["csv","xlsx"])
    right_amount = st.text_input("Right: Amount column", value="amount")
    right_date = st.text_input("Right: Date column", value="date")
    right_ref = st.text_input("Right: Ref/Invoice column (optional)", value="ref")
    right_party = st.text_input("Right: Party column (optional)", value="party")

st.markdown("---")
run = st.button("🔎 Run Reconciliation")

if run and left_file and right_file:
    df_left = load_table(left_file, "csv" if left_file.name.endswith(".csv") else "xlsx")
    df_right = load_table(right_file, "csv" if right_file.name.endswith(".csv") else "xlsx")

    cols_left = {"amount": left_amount, "date": left_date, "ref": left_ref, "party": left_party}
    cols_right = {"amount": right_amount, "date": right_date, "ref": right_ref, "party": right_party}

    matches, exL, exR = reconcile(df_left, df_right, cols_left, cols_right)
    st.success(f"Done. Matches: {len(matches)} | Unmatched (Left): {len(exL)} | Unmatched (Right): {len(exR)}")

    st.subheader("Matches (Top 100)")
    st.dataframe(matches.head(100))

    st.subheader("Unmatched — Left")
    st.dataframe(exL.head(100))

    st.subheader("Unmatched — Right")
    st.dataframe(exR.head(100))

    st.markdown("---")
    st.subheader("3) Generate Certificate/Report")

    company = st.text_input("Company Name", value="Demo Company")
    period = st.text_input("Period", value="FY 2024-25")
    cert_type = st.selectbox("Certificate Template", [
        "Bank Reconciliation Statement (PDF)",
        "Generic Reconciliation Certificate (PDF)",
        "Download Matches (CSV)"
    ])

    if st.button("📄 Generate"):
    if cert_type == "Download Matches (CSV)":
        csv = matches.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download CSV",
            data=csv,
            file_name="recon_matches.csv",
            mime="text/csv",
            key="dl_csv"
        )
    else:
        if cert_type.startswith("Bank Reconciliation"):
            pdf_bytes = generate_bank_reco_pdf_bytes(
                company, period, len(matches), len(exL), len(exR)
            )
            st.download_button(
                "Download PDF",
                data=pdf_bytes,
                file_name="bank_reconciliation_statement.pdf",
                mime="application/pdf",
                key="dl_brs_pdf"
            )
        else:
            notes = f"Matched: {len(matches)} | Unmatched Left: {len(exL)} | Unmatched Right: {len(exR)}"
            pdf_bytes = generate_generic_cert_pdf_bytes(
                "Reconciliation Certificate", company, period, notes
            )
            st.download_button(
                "Download PDF",
                data=pdf_bytes,
                file_name="reconciliation_certificate.pdf",
                mime="application/pdf",
                key="dl_generic_pdf"
            )

st.markdown("---")
st.subheader("Sample Files")
st.write("[Download: Bank_Statement_Sample.csv](./sample_data/Bank_Statement_Sample.csv)")
st.write("[Download: Ledger_Sample.csv](./sample_data/Ledger_Sample.csv)")
