import pandas as pd
from datetime import datetime
from fpdf import FPDF
import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="AI Data Cleaning Assistant", layout="centered")
st.title("🧹 AI Data Cleaning Assistant")

# ================= AUTH =================
if "token" not in st.session_state:
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

    # ---------- LOGIN ----------
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            res = requests.post(
                f"{BACKEND_URL}/auth/login",
                json={"email": email, "password": password}
            )

            if res.status_code == 200:
                st.session_state.token = res.json()["access_token"]
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

    # ---------- REGISTER ----------
    with tab2:
        reg_email = st.text_input("Email", key="reg_email")
        reg_password = st.text_input("Password", type="password", key="reg_pass")

        if st.button("Register"):
            res = requests.post(
                f"{BACKEND_URL}/auth/register",
                json={"email": reg_email, "password": reg_password}
            )

            if res.status_code == 200:
                st.success("Registered successfully. Please login.")
            elif res.status_code == 422:
                st.error("Invalid email or password format")
            else:
                st.error("Registration failed")

    st.stop()

# ================= LOGOUT =================
col1, col2 = st.columns([8, 2])
with col2:
    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()

# 🔐 RAW TOKEN HEADER (matches backend)
def auth_headers():
    return {
        "Authorization": st.session_state.get("token", "")
    }


# ================= UPLOAD & ANALYZE =================
st.subheader("📤 Upload & Analyze CSV")

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file and st.button("Analyze"):
    res = requests.post(
        f"{BACKEND_URL}/upload/analyze",
        headers=auth_headers(),
        files={"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
    )

    if res.status_code == 200:
        data = res.json()
        st.success("Analysis successful")

        st.session_state.temp_id = data["temp_id"]
        st.session_state.suggested_steps = data["suggested_steps"]
        st.session_state.analysis = data["analysis"]
        st.session_state.original_filename = uploaded_file.name
    else:
        st.error(res.text)

# ================= CLEAN =================
if "temp_id" in st.session_state:
    st.subheader("🧹 Clean CSV")

    steps = st.multiselect(
        "Select cleaning steps",
        st.session_state.suggested_steps,
        default=st.session_state.suggested_steps
    )

    if st.button("Clean & Save"):
        res = requests.post(
            f"{BACKEND_URL}/upload/clean/{st.session_state.temp_id}",
            headers=auth_headers(),
            json=steps
        )

        if res.status_code == 200:
            data = res.json()
            cleaned_filename = data["download_url"].split("/")[-1]

            st.session_state.cleaned_filename = cleaned_filename
            st.session_state.applied_steps = steps
            st.session_state.cleaned_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            r = requests.get(
                BACKEND_URL + data["download_url"],
                headers=auth_headers()
            )

            if r.status_code == 200:
                st.session_state.cleaned_file_bytes = r.content
                st.success("Cleaning completed")
            else:
                st.error("Failed to fetch cleaned file")
        else:
            st.error(res.text)

# ================= DOWNLOAD CLEANED =================
if "cleaned_file_bytes" in st.session_state:
    st.download_button(
        "⬇ Download Cleaned CSV",
        st.session_state.cleaned_file_bytes,
        file_name=st.session_state.cleaned_filename,
        mime="text/csv"
    )

# ================= CLEANING SUMMARY =================
if "cleaned_filename" in st.session_state:
    st.subheader("📄 Cleaning Summary")

    summary = {
        "Original File": st.session_state.original_filename,
        "Cleaned File": st.session_state.cleaned_filename,
        "Steps Applied": ", ".join(st.session_state.applied_steps),
        "Analysis": str(st.session_state.analysis),
        "Cleaned At": st.session_state.cleaned_at
    }

    df_summary = pd.DataFrame([summary])
    st.dataframe(df_summary, use_container_width=True)

    # CSV summary
    st.download_button(
        "⬇ Download Summary (CSV)",
        df_summary.to_csv(index=False),
        "cleaning_summary.csv",
        "text/csv"
    )

    # PDF summary
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "AI Data Cleaning Summary", ln=True)
    pdf.ln(5)

    for k, v in summary.items():
        pdf.multi_cell(0, 8, f"{k}: {v}")

    st.download_button(
        "📄 Download Summary (PDF)",
        pdf.output(dest="S").encode("latin-1"),
        "cleaning_summary.pdf",
        "application/pdf"
    )


# ================= HISTORY =================
st.subheader("📁 My Files History")

res = requests.get(
    f"{BACKEND_URL}/files/my",
    headers=auth_headers()
)

if res.status_code != 200:
    st.error("Failed to load history")
else:
    history = res.json()

    if not history:
        st.info("No files found")
    else:
        for f in history:
            st.markdown(f"**Original:** `{f['original_file']}`")
            st.markdown(f"**Cleaned:** `{f['cleaned_file']}`")

            c1, c2 = st.columns(2)

            with c1:
                if st.button("⬇ Cleaned", key=f"c_{f['id']}"):
                    r = requests.get(
                        f"{BACKEND_URL}/files/download/{f['cleaned_file']}",
                        headers=auth_headers()
                    )
                    if r.status_code == 200:
                        st.download_button(
                            "Save Cleaned CSV",
                            r.content,
                            f["cleaned_file"],
                            "text/csv",
                            key=f"sc_{f['id']}"
                        )

            with c2:
                if st.button("⬇ Original", key=f"o_{f['id']}"):
                    r = requests.get(
                        f"{BACKEND_URL}/files/download/original/{f['original_file']}",
                        headers=auth_headers()
                    )
                    if r.status_code == 200:
                        st.download_button(
                            "Save Original CSV",
                            r.content,
                            f["original_file"],
                            "text/csv",
                            key=f"so_{f['id']}"
                        )

            st.divider()
