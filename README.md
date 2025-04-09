# 🌺 SereniStay Technical Document

Welcome to the technical documentation of **SereniStay**, a restful API designed to manage serene stays and peaceful bookings.
This document covers the architecture, routes, CRUD operations, database integration, and other key components that power the backend of SereniStay.

---

# 📑 Table of Contents

1. [Introduction](#introduction)
2. [Technologies used](#technologies-used)
3. [Business Logic Layer](#business-logic-layer)
4. [Project Structure Overview](#project-structure-overview)
5. [Authentication & Authorization](#authentication-&-authorization)
6. [Roles Overview](#roles-overview)
7. [API Endpoint Tests](#API-endpoint-tests)
8. [Known Limitations](#know-limitatoins)
9. [Final Notes](#final-notes)

---

# 📖 Introduction

**SereniStay** is a RESTful API that manages reservations for quiet stays. This backend provides functionality for creating, querying, updating, and deleting data related to users, accommodations, reservations, and more.

> ⚠️ **Note:** SereniStay is a Minimum Viable Product (MVP).

---

# ⚙️ Technologies used

- **Python** - Programming language used to build the API.
- **FastAPI** – Modern web framework for building fast APIs with automatic documentation.
- **MongoDB** – Non-relational (NoSQL) database used for storing application data.
- **Pydantic** - Data validation library used with FastAPI to ensure request and response integrity.
- **Uvicorn** - ASGI server for running the FastAPI application.
- **CORS Middleware** - Enables secure communication between the backend and frontend applications.

---

## 🧠 Business Logic Layer

**SereniStay** follows a modular architecture that separates responsibilities across different layers, making the project scalable and easy to maintain.

---

# 🗂️ Project Structure Overview

| Path                      | Description                                      |
|---------------------------|--------------------------------------------------|
| `app/api/`                | Routes grouped by version (v1 endpoints).        |
| `app/models/`             | Pydantic models and domain entities.             |
| `app/persistence/`        | Interfaces for interacting with the database.    |
| `app/services/`           | Core business logic.                             |
| `app/db.py`               | MongoDB connection setup.                        |
| `run.py`                  | Entry point for running the application.         |
| `Dockerfile`              | Docker configuration.                            |
| `requirements.txt`        | Project dependencies.                            |
| `app/__init__.py`         | FastAPI app initialization, CORS setup, and router inclusion. |

---

# 🔐 Authentication & Authorization

SereniStay uses JWT (JSON Web Tokens) to securely manage user sessions. The authentication process is built using `OAuth2PasswordBearer`, and permissions are controlled by roles defined in the user model.

---

# 👤 Roles Overview

| Role                     | Capabilities                                     |
|---------------------------|--------------------------------------------------|
| `Owner`                | Create spas, list users, manage everything.        |
| `Client`             | Book services, see available spas.             |

---

# 🧪 API Endpoint Tests (Examples)

🧾 POST /register – Register a new user
  - **Request**
```
{   
  "first_name": "Christopher",
  "last_name": "Morales",
  "email": "cmorales@gmail.com",
  "role": "Owner",
  "password": "SecurePass123"
}
```
  - **Response**
```
{
    "message": "Successfully registered user",
    "id": "76c6e9a9-81c6-4e47-ab97-b5c7580d138d"
}
```
  - **Status**
```
"POST /login HTTP/1.1" 200 OK
```
---

🔐 **POST /login – User Login**
  - **Request**
```
{   
  "email": "cmorales@gmail.com",
  "password": "SecurePass123"
}
```
  - **Response**
```
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjbW9yYWxlc0BnbWFpbC5jb20iLCJyb2xlIjoiT3duZXIiLCJleHAiOjE3NDQyMzQ4ODl9.Ek-HF57OOmrgB3AvarF7KX7NzDEwd4dD15zuPMCid3k",
  "token_type": "bearer"
}
```
  - **Status**
```
"POST /login HTTP/1.1" 200 OK
```
---

🏨 POST /api/v1/create_spa – Create new spa
> ⚠️ **Note:** To create a spa, you must be an owner.
  - **Request**
```
{
  "title": "Relax",
  "description": "Disfruta de nuestros servicios de spa que incluyen masajes, faciales y más para relajarte y revitalizarte.",
  "address": "123 Serenity Blvd",
  "services": [
    {
      "name": "Masaje corporal completo",
      "duration": 60,
      "price": 30.000
    },
    {
      "name": "Facial rejuvenecedor",
      "duration": 45,
      "price": 10.000
    }
  ]
}
```
  - **Response**
```
{
  "id": "e0103e00-4c06-4e45-8df9-1ff39385a996",
  "created_at": "2025-04-09T20:52:15.148000",
  "updated_at": "2025-04-09T20:52:15.148000",
  "title": "Relax",
  "description": "Disfruta de nuestros servicios de spa que incluyen masajes, faciales y más para relajarte y revitalizarte.",
  "address": "123 Serenity Blvd"
}
```
  - **Status**
```
"POST /api/v1/create_spa HTTP/1.1" 200 OK
```

---
⏰ **POST /api/v1/create_booking – Create a reservation**
  - **Request**
```
{
  "spa_id": "e0103e00-4c06-4e45-8df9-1ff39385a996",
  "user_id": "6c3f0119-7c00-41af-98c4-ebe84fee32af",
  "services_id": [
    "325f05f0-2d42-4ed8-b437-131d04095906"
  ],
  "reservation_datetime": "2025-04-10T14:00:00",
  "status": "pending"
}
```
  - **Response**
```
{
    "success": "Reserve created",
    "booking_id": "67f6e1f5d8c8696f464c9208"
}
```
  - **Status**
```
"POST /api/v1/create_booking HTTP/1.1" 200 OK
```

---
❌ **PUT /api/v1/cancel_booking/{booking_id}/cancel – Cancel a reservation**
  - **Request**
```
http://localhost:4000/api/v1/cancel_booking/007d6b33-3046-4251-909b-ab24b7171431/cancel
```
  - **Response**
```
{
    "success": "Reservation cancelled successfully"
}
```
  - **Status**
```
"PUT /api/v1/cancel_booking/007d6b33-3046-4251-909b-ab24b7171431/cancel HTTP/1.1" 200 OK
```

---
📄 **GET /api/v1/spas – Get all spas**
  - **Request**
```
http://localhost:4000/api/v1/spas
```
  - **Response**
```
[
  {
    "id": "23a0893e-53e6-49fc-9917-0830f0b1bbe6",
    "created_at": "2025-03-27T14:09:18.563000",
    "updated_at": "2025-03-27T14:09:18.563000",
    "title": "Relax",
    "description": "Disfruta de nuestros servicios de spa que incluyen masajes, faciales y más para relajarte y revitalizarte.",
    "address": "123 Serenity Blvd",
    "services": []
  },
  {
    "id": "d3a6dc85-83c5-47b5-a121-93df88aa3f56",
    "created_at": "2025-03-27T19:56:30.793000",
    "updated_at": "2025-03-27T19:56:30.793000",
    "title": "SereniSpa",
    "description": "Contamos con servicios de calidad, ven y disfruta",
    "address": "Address - 50 / 20",
    "services": []
  }
]
```
  - **Status**
```
"GET /api/v1/spas HTTP/1.1" 200 OK
```

---
📄 **GET /api/v1/users – Get all users**
> ⚠️ **Note:** To list all users, you must be an owner.
  - **Request**
```
http://localhost:4000/api/v1/users
```
  - **Response**
```
[
  {
    "id": "6c3f0119-7c00-41af-98c4-ebe84fee32af",
    "created_at": "2025-03-27T14:05:10.625000",
    "updated_at": "2025-03-27T14:05:10.625000",
    "first_name": "Christopher",
    "middle_name": null,
    "last_name": "Morales",
    "email": "cmorales@gmail.com",
    "role": "Owner",
    "hashed_password": "$2b$12$6y9kg2sMhSCbmP5GanTx1epWfhQFmLBZXbv0APsYuau9cs9UxBvS6"
  },
  {
    "id": "06cdaf40-94d5-4ede-9000-878b965a9bd0",
    "created_at": "2025-03-27T16:39:48.243000",
    "updated_at": "2025-03-27T16:39:48.243000",
    "first_name": "Camilo",
    "middle_name": null,
    "last_name": "Montoya",
    "email": "cmontoya@gmail.com",
    "role": "Client",
    "hashed_password": "$2b$12$oedJ2iZQd79eHQBpkXF9S.MZh1m4w06Ee7U8.yegAWYHa1zB9N8Pe"
  }
]
```
  - **Status**
```
"GET /api/v1/users HTTP/1.1" 200 OK
```

---

# 🚧 Known Limitations

As this is a Minimum Viable Product (MVP), some features are not yet implemented:

- 🔁 No check for duplicate users on registration.
- 📝 The functionality of making reviews should be added.
- ✅ Make it easier to make reservations.
- 🔐 There must be another role, who can see the users.
- 🗑️ Ability to delete users and spas.
- ♻️ Add filters for search spas

---

## Author

**Christopher Morales Torres**
- Email: christophermoralestorres@gmail.com
- Linkedin: www.linkedin.com/in/christopher-morales-torres-5823032ab
