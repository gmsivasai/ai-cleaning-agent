from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.database import Base, engine
from app.auth.router import router as auth_router
from app.upload.router import router as upload_router
from app.upload.history_router import router as history_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Data Cleaning Assistant")

app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(history_router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title="AI Data Cleaning Assistant",
        version="1.0.0",
        routes=app.routes,
    )

    schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = schema
    return schema

app.openapi = custom_openapi
