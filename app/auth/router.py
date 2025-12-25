from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.auth.schemas import UserRegister, UserLogin, Token
from app.auth.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    email = user.email.strip().lower()

    # 🚫 HARD BLOCK empty or whitespace password
    if not user.password or not user.password.strip():
        raise HTTPException(
            status_code=400,
            detail="Password cannot be empty"
        )

    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(user.password)

    new_user = User(
        email=email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}
@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    email = user.email.strip().lower()

    if not user.password or not user.password.strip():
        raise HTTPException(
            status_code=400,
            detail="Password cannot be empty"
        )

    db_user = db.query(User).filter(User.email == email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    

    return {
        "access_token": create_access_token(email),  # ✅ FIXED
        "token_type": "bearer"
    }
