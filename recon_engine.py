
import pandas as pd
from datetime import datetime
try:
    from rapidfuzz import fuzz
except Exception:
    fuzz = None

def load_table(file, filetype=None, sheet_name=0):
    if filetype is None:
        name = getattr(file, "name", str(file)).lower()
        if name.endswith(".csv"):
            filetype = "csv"
        elif name.endswith(".xlsx") or name.endswith(".xls"):
            filetype = "xlsx"
        else:
            filetype = "csv"
    if filetype == "csv":
        return pd.read_csv(file)
    else:
        return pd.read_excel(file, sheet_name=sheet_name)

def normalize_amount(x):
    try:
        return round(float(str(x).replace(",","").strip()), 2)
    except:
        return None

def to_date(x):
    for fmt in ("%Y-%m-%d","%d-%m-%Y","%d/%m/%Y","%m/%d/%Y","%d %b %Y","%d %B %Y"):
        try:
            return datetime.strptime(str(x).strip(), fmt).date()
        except:
            continue
    return None

def reconcile(df_left, df_right, cols_left, cols_right, allow_fuzzy=True, date_tolerance_days=3):
    A = df_left.copy()
    B = df_right.copy()

    A["_amt"] = A[cols_left["amount"]].apply(normalize_amount)
    B["_amt"] = B[cols_right["amount"]].apply(normalize_amount)

    A["_date"] = A[cols_left["date"]].apply(to_date) if cols_left.get("date") in A.columns else None
    B["_date"] = B[cols_right["date"]].apply(to_date) if cols_right.get("date") in B.columns else None

    A["_ref"] = A[cols_left.get("ref","")] if cols_left.get("ref","") in A.columns else ""
    B["_ref"] = B[cols_right.get("ref","")] if cols_right.get("ref","") in B.columns else ""

    A["_party"] = A[cols_left.get("party","")] if cols_left.get("party","") in A.columns else ""
    B["_party"] = B[cols_right.get("party","")] if cols_right.get("party","") in B.columns else ""

    matches = []
    used_B = set()

    for i, rowA in A.iterrows():
        amtA = rowA["_amt"]
        dateA = rowA["_date"]
        refA  = str(rowA["_ref"])
        partyA= str(rowA["_party"])

        if amtA is None: 
            continue

        cand = B[(B["_amt"] == amtA) & (~B.index.isin(used_B))]

        best_idx = None
        best_score = -1

        for j, rowB in cand.iterrows():
            score = 0
            dateB = rowB.get("_date", None)
            refB  = str(rowB.get("_ref", ""))
            partyB= str(rowB.get("_party",""))

            if dateA and dateB:
                try:
                    delta = abs((dateA - dateB).days)
                    score += max(0, (date_tolerance_days - delta))
                except:
                    pass

            if allow_fuzzy and fuzz:
                score += fuzz.partial_ratio(refA, refB)/100.0
                score += fuzz.partial_ratio(partyA, partyB)/100.0
            else:
                score += 1.0 if refA and refA == refB else 0.0
                score += 1.0 if partyA and partyA == partyB else 0.0

            if score > best_score:
                best_score = score
                best_idx = j

        if best_idx is not None:
            used_B.add(best_idx)
            matches.append({
                "A_index": i,
                "B_index": best_idx,
                "amount": amtA,
                "score": round(best_score, 2),
                "A_row": rowA.to_dict(),
                "B_row": B.loc[best_idx].to_dict()
            })

    matched_A = set([m["A_index"] for m in matches])
    matched_B = set([m["B_index"] for m in matches])

    exceptions_left  = A[~A.index.isin(matched_A)]
    exceptions_right = B[~B.index.isin(matched_B)]

    return pd.DataFrame(matches), exceptions_left, exceptions_right
