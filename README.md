# Finance Dashboard Backend

A robust backend system for a Finance Dashboard built with **Django REST Framework** using only `APIView` (no ViewSets). The system supports role-based access control, financial record management, and dashboard analytics with **PostgreSQL (Neon)** as the database.

---

## Objective
This backend demonstrates proper API design, data modeling, business logic, role-based access control, and clean architecture for a finance dashboard application.

---

## Features

- **User & Role Management** (Admin, Analyst, Viewer)
- **Financial Records CRUD** with proper ownership
- **Dashboard Summary Analytics**
  - Total Income, Total Expense, Net Balance
  - Category-wise breakdown
- **Role-Based Access Control**
  - Viewer: Can only view records and dashboard
  - Analyst: Can view + create/update records
  - Admin: Full access (create, update, delete, manage users)
- **JWT Authentication**
- **Input Validation & Proper Error Handling**
- **Filtering & Search Support**
- **Swagger API Documentation**

---

## Tech Stack

- **Backend**: Django 5.1 + Django REST Framework
- **Database**: PostgreSQL (Neon Serverless)
- **Authentication**: JWT (SimpleJWT)
- **Documentation**: drf-spectacular (Swagger UI)
- **Environment Management**: python-decouple

---

## Project Structure

```bash
finance_dashboard_backend/
├── finance_dashboard/          # Django settings & main urls
├── accounts/                   # User registration & model
├── records/                    # Financial records APIs
├── dashboard/                  # Dashboard summary API
├── core/                       # Custom permissions
├── .env
├── requirements.txt
├── README.md
└── manage.py
```

---

## Setup Instructions

### 1. Clone & Setup Environment

```bash
git clone <your-repo-url>
cd finance_dashboard_backend

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create `.env` file in the root directory:

```env
SECRET_KEY=your-super-secret-key-here-make-it-strong
DEBUG=True

# Neon PostgreSQL Credentials
DB_NAME=neondb
DB_USER=your_neon_username
DB_PASSWORD=your_neon_password
DB_HOST=your-project.neon.tech
DB_PORT=5432
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the Server

```bash
python manage.py runserver
```

Server will run at: `http://127.0.0.1:8000`

---

## API Endpoints

| Method | Endpoint                        | Description                        | Access              |
|--------|---------------------------------|------------------------------------|---------------------|
| POST   | `/api/token/`                   | Login & get JWT tokens             | Public              |
| POST   | `/api/auth/register/`           | Register new user                  | Public              |
| GET    | `/api/records/`                 | List user's financial records      | All authenticated   |
| POST   | `/api/records/`                 | Create new record                  | Analyst + Admin     |
| GET    | `/api/records/<id>/`            | Get single record                  | All authenticated   |
| PUT    | `/api/records/<id>/`            | Update record                      | Analyst + Admin     |
| DELETE | `/api/records/<id>/`            | Delete record                      | Admin only          |
| GET    | `/api/dashboard/summary/`       | Get dashboard summary              | All authenticated   |

**API Documentation**:  
- Swagger UI → `/api/docs/`

---

## Roles & Permissions

| Role       | View Records | Create/Update | Delete Records | Dashboard Access |
|------------|--------------|---------------|----------------|------------------|
| **Viewer** | Yes          | No            | No             | Yes              |
| **Analyst**| Yes          | Yes           | No             | Yes              |
| **Admin**  | Yes          | Yes           | Yes            | Yes              |

---

## Postman Testing Guide (Complete)

**Base URL**: `http://127.0.0.1:8000`

### 1. Register Users

**Register Admin**
```json
POST {{base_url}}/api/auth/register/
{
  "email": "admin@example.com",
  "username": "admin",
  "password": "admin123",
  "role": "admin"
}
```

**Register Analyst**
```json
POST {{base_url}}/api/auth/register/
{
  "email": "analyst@example.com",
  "username": "analyst",
  "password": "analyst123",
  "role": "analyst"
}
```

**Register Viewer**
```json
POST {{base_url}}/api/auth/register/
{
  "email": "viewer@example.com",
  "username": "viewer",
  "password": "viewer123",
  "role": "viewer"
}
```

### 2. Login (Get JWT Token)

**Login as Admin / Analyst / Viewer**
```json
POST {{base_url}}/api/token/
{
  "email": "admin@example.com",
  "password": "admin123"
}
```

→ Copy the **`access`** token and use it in the `Authorization` header as `Bearer <token>`

### 3. Add Categories (Important)

1. Open Django Admin: `http://127.0.0.1:8000/admin/`
2. Login with Admin credentials
3. Add the following Categories:

   **Income Categories**:
   - `Salary` (income)
   - `Freelance` (income)
   - `Investment` (income)

   **Expense Categories**:
   - `Food` (expense)
   - `Rent` (expense)
   - `Transport` (expense)
   - `Shopping` (expense)

### 4. Financial Records Testing

**Create Income Record**
```json
POST {{base_url}}/api/records/
Authorization: Bearer {{access_token}}

{
  "amount": 75000,
  "type": "income",
  "category": 1,
  "date": "2026-04-01",
  "description": "April Monthly Salary"
}
```

**Create Expense Record**
```json
POST {{base_url}}/api/records/
Authorization: Bearer {{access_token}}

{
  "amount": 12000,
  "type": "expense",
  "category": 5,
  "date": "2026-04-05",
  "description": "Monthly House Rent"
}
```

**List All Records**
```json
GET {{base_url}}/api/records/
Authorization: Bearer {{access_token}}
```

**Update Record**
```json
PUT {{base_url}}/api/records/1/
Authorization: Bearer {{access_token}}

{
  "amount": 80000,
  "description": "Updated April Salary"
}
```

**Delete Record (Only Admin)**
```json
DELETE {{base_url}}/api/records/1/
Authorization: Bearer {{access_token}}
```

### 5. Dashboard Summary

```json
GET {{base_url}}/api/dashboard/summary/
Authorization: Bearer {{access_token}}
```

**Expected Response Example**:
```json
{
  "total_income": 75000,
  "total_expense": 12000,
  "net_balance": 63000,
  "total_records": 2,
  "category_summary": [
    { "category__name": "Salary", "type": "income", "total": 75000 },
    { "category__name": "Rent", "type": "expense", "total": 12000 }
  ]
}
```

### 6. Access Control Testing (Must Test)

- Login as **Viewer** → Try to **POST** `/api/records/` → Should return **403 Forbidden**
- Login as **Analyst** → Try to **DELETE** a record → Should return **403 Forbidden**
- Login as **Admin** → All operations should work

---

## Assumptions Made

- Each user can only access and manage **their own** financial records
- Categories are managed globally via Django Admin
- Amount must always be positive; `type` field decides income or expense
- No pagination or soft delete (kept simple for assignment)

---

**Developed for Backend Assignment Evaluation**
