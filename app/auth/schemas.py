from pydantic import BaseModel, EmailStr, Field

# =============================
# REGISTER SCHEMA
# =============================
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

# =============================
# LOGIN SCHEMA
# =============================
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# =============================
# TOKEN RESPONSE SCHEMA
# =============================
class Token(BaseModel):
    access_token: str
    token_type: str
