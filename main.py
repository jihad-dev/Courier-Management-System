from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ১. Middleware ইমপোর্ট করুন
from database import engine, Base
from router import auth, admin, user

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Courier & Logistics Management API", version="1.0.0")

# ২. CORS Middleware কনফিগারেশন (এটি যুক্ত করুন)
origins = [
    "http://localhost:5173",  # Vite Frontend URL
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  
)

# ৩. রাউটারসমূহ
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(user.router)


@app.get("/")
def home():
    return {"message": "Welcome to Courier & Logistics Management API"}
