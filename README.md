AI Data Cleaning Assistant

An end-to-end **AI-powered CSV Data Cleaning Assistant** that allows users to securely upload messy datasets, analyze common data quality issues, apply intelligent cleaning steps, and download cleaned files — all through a simple web interface.

---

## 📌 Features

### 🔐 Authentication & Security

* User **registration and login**
* **JWT-based authentication**
* Password hashing using **bcrypt**
* Input validation using **Pydantic**
* Protected routes with per-user file access

---

### 📤 CSV Upload & Analysis

* Upload raw / messy CSV files
* Automatic detection of:

  * Missing values
  * Duplicate rows
  * Data types and inconsistencies
* Analysis results returned instantly

---

### 🧠 Intelligent Cleaning

* Smart cleaning agent (no ML models required)
* Supported cleaning steps:

  * Fill missing values
  * Remove duplicate rows
* User-selectable cleaning workflow
* Cleaned files stored securely per user

---

### 📥 Downloads & History

* Download **cleaned CSV**
* Download **original CSV**
* View complete **file history**
* Secure access — users can only download their own files

---

### 📄 Cleaning Summary (Frontend-Only)

* Auto-generated cleaning summary
* Export summary as:

  * CSV
  * PDF
* No backend changes required for summary export

---

## 🧰 Tech Stack

### Backend

* **FastAPI** (async REST API)
* **SQLAlchemy + PostgreSQL**
* **JWT authentication**
* **Pydantic validation**
* **Pandas** for data processing

### Frontend

* **Streamlit**
* REST API integration using `requests`

### Security

* Password hashing: `passlib (bcrypt)`
* Token handling: `python-jose`

---

## 📁 Project Structure

```
ai-data-cleaning-backend/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   │
│   ├── auth/
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── deps.py
│   │   └── security.py
│   │
│   ├── upload/
│   │   ├── router.py
│   │   ├── temp_store.py
│   │   └── history_router.py
│   │
│   └── cleaning/
│       ├── analyze.py
│       └── agent.py
│
├── uploads/          # original CSV files
├── cleaned/          # cleaned CSV files
│
├── frontend_streamlit.py
├── requirements.txt
├── run_app.bat
├── stop_app.bat
└── README.md
```

---

## ▶️ How to Run the Application

### 1️⃣ Activate virtual environment

```bash
venv\Scripts\activate
```

### 2️⃣ Start backend

```bash
python -m uvicorn app.main:app --reload
```

### 3️⃣ Start frontend

```bash
streamlit run frontend_streamlit.py
```

OR (recommended):

```bash
run_app.bat
```

---

## 🛑 Stop the Application

```bash
stop_app.bat
```

Safely stops both FastAPI and Streamlit processes.

---

## 🧪 Demo Flow

1. Register a new user
2. Login
3. Upload a messy CSV file
4. Analyze dataset
5. Select cleaning steps
6. Clean & save file
7. Download cleaned CSV
8. View file history
9. Export cleaning summary (CSV / PDF)
10. Logout

---

## 🔒 Validation Rules

* Email must be valid (`EmailStr`)
* Password:

  * Minimum **6 characters**
  * Cannot be empty or whitespace
* Unauthorized users cannot access files
* JWT tokens validated on every protected request

---

## 🧠 Design Highlights

* **Separation of concerns**

  * Validation → Pydantic
  * Business logic → Routers
  * Security → JWT + hashing
  * UI → Streamlit
* No frontend logic leaks into backend
* No backend changes required for UI enhancements

---

## 🚀 Future Enhancements (Optional)

* Password strength meter
* Strong password regex rules
* LangGraph-based multi-step cleaning orchestration
* Cloud storage (AWS S3)
* Admin dashboard
* Rate-limiting on login attempts

---

## 👨‍💻 Author

**Sivasai**
AI Data Cleaning Assistant Project

---
🎥 Demo Video:
https://drive.google.com/file/d/1BVzVAc6p_DW9spSXgeEb0y8jKNNjdc5N/view?usp=sharing

