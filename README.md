🚚 Courier & Logistics Management Platform API

A robust, production-ready RESTful API backend for a modern Courier & Logistics Management Platform built with Python, FastAPI, SQLAlchemy, and SQLite.

This system handles end-to-end logistics operations including multi-role authentication (Customer, Admin, Rider), parcel booking, status tracking, automated tracking ID generation, complex search/filtering, and pagination.

🌟 Key Features

🔐 Authentication & Security

JWT Authentication: Secure user registration and login using JSON Web Tokens.

Password Hashing: Passwords securely hashed with bcrypt.

Role-Based Access Control (RBAC): Distinct permissions for CUSTOMER, ADMIN, and RIDER roles.

Forgot & Reset Password: Token-based password recovery workflow.

📦 Parcel & Logistics Management

Automated Tracking ID: Unique tracking code (TRK-XXXXXXXX) generated for every parcel.

Lifecycle Tracking: Track parcels through statuses: PENDING ➔ PICKED_UP ➔ IN_TRANSIT ➔ DELIVERED / CANCELLED.

Customer Actions: Book parcels, view personal delivery history, track parcel status, and cancel pending orders.

Admin Controls: Assign riders, update delivery status, manage all parcels, and control system users.

🔎 Advanced Data Querying

Search: Search parcels by Tracking ID or Recipient Name.

Multi-Filter: Filter by parcel status (PENDING, DELIVERED, etc.), category (Electronics, Document, etc.), or creation date range.

Sorting: Sort datasets dynamically by date (created_at), delivery charge, or recipient name in ASC/DESC order.

Pagination: Configurable page sizes and pagination metadata (page, page_size, total_pages, total).

🛠️ Tech Stack

Framework: FastAPI

Language: Python 3.10+

Database: SQLite (via SQLAlchemy ORM)

Data Validation: Pydantic v2 & email-validator

Authentication: python-jose (JWT), passlib[bcrypt]

📂 Project Structure

.
├── database.py       # Database connection & session setup
├── models.py         # SQLAlchemy database models & enums
├── main.py           # FastAPI application entry point
├── requirements.txt  # Python dependencies
└── router/           # API Route handlers
    ├── admin.py      # Admin management & extended parcel listing
    ├── auth.py       # Authentication, login, signup & password reset
    └── user.py       # Customer booking, listing & tracking endpoints


🚀 Getting Started

1. Prerequisites

Ensure you have Python 3.10+ installed on your system.

2. Clone the Repository

git clone https://github.com/your-username/courier-logistics-backend.git
cd courier-logistics-backend


3. Create a Virtual Environment

# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate


4. Install Dependencies

pip install -r requirements.txt


5. Run the Application

uvicorn main:app --reload


The server will start at http://127.0.0.1:8000.

📖 API Documentation

FastAPI automatically generates interactive API documentation. Once the app is running, visit:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

🧪 Sample Request Payload

Book a Parcel (POST /user/parcels or POST /admin/parcels)

{
  "recipient_name": "Tanvir Hossain",
  "recipient_phone": "01712345678",
  "pickup_address": "House 12, Road 5, Dhanmondi, Dhaka",
  "delivery_address": "Flat 4B, Green Villa, Nasirabad, Chattogram",
  "category": "Electronics",
  "weight_kg": 1.5,
  "delivery_charge": 150.0
}


📜 License

This project is open-source and available under the MIT License.
