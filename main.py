from fastapi import FastAPI
from database import engine, Base
from router import auth, admin, user  # user import করুন

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Courier & Logistics Management API",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(user.router)  

@app.get("/")
def home():
    return {"message": "Welcome to Courier & Logistics Management API"}