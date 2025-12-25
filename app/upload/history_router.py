from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os

from app.database import get_db
from app.auth.deps import get_current_user_email
from app.models import FileHistory

router = APIRouter(prefix="/files", tags=["Files"])


@router.get("/my")
def get_my_files(
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user_email)
):
    return (
        db.query(FileHistory)
        .filter(FileHistory.user_email == user_email)
        .order_by(FileHistory.created_at.desc())
        .all()
    )


@router.get("/download/{filename}")
def download_file(
    filename: str,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user_email)
):
    # 🔒 Check ownership in DB
    record = db.query(FileHistory).filter(
        FileHistory.cleaned_file == filename,
        FileHistory.user_email == user_email
    ).first()

    if not record:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this file"
        )

    path = os.path.join("cleaned", filename)

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path,
        media_type="text/csv",
        filename=filename
    )
@router.get("/download/original/{filename}")
def download_original_file(
    filename: str,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user_email)
):
    record = db.query(FileHistory).filter(
        FileHistory.original_file == filename,
        FileHistory.user_email == user_email
    ).first()

    if not record:
        raise HTTPException(403, "Not authorized")

    path = os.path.join("uploads", filename)
    if not os.path.exists(path):
        raise HTTPException(404, "File not found")

    return FileResponse(path, media_type="text/csv", filename=filename)
