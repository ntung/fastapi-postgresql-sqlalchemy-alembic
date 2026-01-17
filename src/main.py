import os
from fastapi import FastAPI

from src.routers.auth_routes import auth_router
from src.routers.user_routes import user_router
from src.routers.book_routes import book_router
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(debug=os.getenv("DEBUG", "False").lower() == "true")
app.include_router(book_router)
app.include_router(auth_router)
app.include_router(user_router)


@app.get("/")
def root():
    return {"message": "FastAPI Auth API", "docs": "/docs"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
