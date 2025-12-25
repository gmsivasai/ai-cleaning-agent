from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
import pandas as pd
import os
from uuid import uuid4
from datetime import datetime
from pandas.errors import EmptyDataError
from app.cleaning.analyze import analyze_csv
from app.cleaning.agent import clean_csv
from app.auth.deps import get_current_user_email
from app.upload.temp_store import TEMP_FILES
from app.database import SessionLocal
from app.models import CleaningHistory, FileHistory

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = "uploads"
CLEANED_DIR = "cleaned"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CLEANED_DIR, exist_ok=True)
@router.post("/analyze")
def analyze_file(
    file: UploadFile = File(...),
    user_email: str = Depends(get_current_user_email)
):
    path = os.path.join(UPLOAD_DIR, file.filename)

    # Save file
    with open(path, "wb") as f:
        f.write(file.file.read())

    # ✅ SAFE CSV LOAD
    try:
        df = pd.read_csv(path)
    except EmptyDataError:
        raise HTTPException(
            status_code=400,
            detail="Uploaded CSV file is empty"
        )

    # ✅ Handle header-only CSV
    if df.empty:
        raise HTTPException(
            status_code=400,
            detail="CSV file contains no data rows"
        )

    temp_id = str(uuid4())

    TEMP_FILES[temp_id] = {
        "df": df,
        "filename": file.filename,
        "user_email": user_email
    }

    return {
        "temp_id": temp_id,
        "analysis": analyze_csv(df),
        "suggested_steps": ["fill_missing_values", "remove_duplicates"]
    }


@router.post("/clean/{temp_id}")
def clean_file(
    temp_id: str,
    steps: list[str],
    user_email: str = Depends(get_current_user_email)
):
    temp = TEMP_FILES.get(temp_id)
    if not temp or temp["user_email"] != user_email:
        raise HTTPException(403, "Unauthorized")

    df, applied = clean_csv(temp["df"], steps)

    name = f"cleaned_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{temp['filename']}"
    path = os.path.join(CLEANED_DIR, name)
    df.to_csv(path, index=False)

    db = SessionLocal()
    db.add(FileHistory(
        user_email=user_email,
        original_file=temp["filename"],
        cleaned_file=name,
        steps="\n".join(applied)
    ))
    db.add(CleaningHistory(
        user_email=user_email,
        original_filename=temp["filename"],
        cleaned_filename=name,
        steps="\n".join(applied)
    ))
    db.commit()
    db.close()

    del TEMP_FILES[temp_id]

    return {"download_url": f"/upload/download/{name}"}

@router.get("/download/{filename}")
def download(filename: str):
    return FileResponse(
        os.path.join(CLEANED_DIR, filename),
        media_type="text/csv",
        filename=filename
    )
