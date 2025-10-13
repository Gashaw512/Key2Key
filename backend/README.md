# 🚀 Key2Key Backend (FastAPI)

The **Key2Key Backend** is a production-grade service built using **FastAPI**, **SQLModel**, and **PostgreSQL**.  
It is architected for **scalability**, **security**, and **performance**, powering the core logic of the Key2Key ecosystem.

---

## 🛠️ Getting Started


### 1. Prerequisites

Ensure you have the following installed on your machine:

- **Python 3.8+**
- **PostgreSQL** (if using PostgreSQL)

To install PostgreSQL on Ubuntu, run:

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```
### 2. Starting PostgreSQL

Once PostgreSQL is installed, you need to start the service and set up the database.

1. **Start PostgreSQL Service**:

   ```bash
   sudo service postgresql start
   ```
2. **Check PostgresQL Status**:
   ```bash
   sudo service postgresql status
   ```
4. **Access PostgresQL Shell**:
   ```bash
   sudo -i -u postgres
   psql
   ```
6. **Create User and Database**
   
   ```bash
   CREATE USER gashaw WITH PASSWORD '1234';
   CREATE DATABASE key2key WITH OWNER gashaw;
   GRANT ALL PRIVILEGES ON DATABASE key2key TO gashaw;
   ```

### 3. Environment Setup

Begin by creating and activating a dedicated Python virtual environment to manage dependencies.

```bash
# Create a virtual environment
python -m venv .venv

# Activate (macOS/Linux)
source .venv/bin/activate

# Activate (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

```
### 4. Install Dependencies

Install the required packages using **pip**.

```bash
pip install -r requirements.txt
```

### 5. Configuration

Configure the service by setting up necessary environment variables in a local `.env` file.

First, copy the example file:

```bash
cp .env.example .env
```
Then edit .env and replace SECRET_KEY with a secure token:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
Paste the generated key into your .env file.
###  🧠 5. Running the Application
Start the FastAPI development server:
```bash
uvicorn app.main:app --reload
```
### Access Points

The API will now be accessible at `http://127.0.0.1:8000`.

| Documentation | URL |
| :--- | :--- |
| **Swagger UI** (Interactive Docs) | `http://127.0.0.1:8000/docs` |
| **ReDoc** (Formal Docs) | `http://127.0.0.1:8000/redoc` |

## 🔒 Authentication Flow Testing

Follow these steps to test the user registration and JWT token retrieval.

### Step 1: Register a User

Execute a `POST` request to the registration endpoint with the desired user details.

`POST /api/v1/auth/register`

Example Request Body (JSON):

```json
{
  "full_name": "Gashaw",
  "email": "you@example.com",
  "password": "Str0ngPass!"
}
```
### Step 2: Log In and Get a Token

After successful registration, perform a login request using the credentials.

**Note:** FastAPI's default login uses `application/x-www-form-urlencoded` data (form data), not JSON.

Example Form Data:

| Key | Value |
| :--- | :--- |
| `username` | `you@example.com` |
| `password` | `Str0ngPass!` |

A successful login will return a **JWT Access Token** that must be included in the `Authorization` header of subsequent protected requests (e.g., `Authorization: Bearer <YOUR_JWT_TOKEN>`).

# 🏗️ Project Architecture & Roadmap

A professional, scalable FastAPI project structure with modular services, APIs, and testing, ready for production-grade development.

---

## 🧱 1. Full Project Structure

```text
app/
├── __init__.py
├── main.py
├── core/
│   ├── __init__.py
│   ├── config.py          # Global settings & environment variables
│   ├── database.py        # SQLAlchemy engine, session, base
│   ├── security.py        # Password hashing & token generation
│   ├── jwt.py             # JWT encode/decode logic
│   ├── auth_backend.py    # OAuth2/JWT integration with FastAPI
│   ├── caching.py         # Redis cache setup & utilities
│   ├── payments.py        # Payment gateway integrations
│   ├── tasks.py           # Celery tasks (async background jobs)
│   ├── logging_config.py  # Logging setup & formatters
│   ├── utils.py           # Helper functions
│   └── middleware.py      # Request/response middlewares

├── db/
│   ├── __init__.py
│   ├── session.py         # DB session management
│   ├── base_class.py      # Declarative Base for SQLAlchemy models
│   ├── init_db.py         # Seed / initial data creation
│   └── migrations/        # Alembic migration folder

├── models/
│   ├── __init__.py
│   ├── user.py            # User model
│   ├── broker.py
│   ├── listing.py
│   ├── vehicle.py
│   ├── property.py
│   ├── payment.py
│   ├── chat.py
│   ├── notification.py
│   ├── verification.py
│   ├── analytics.py
│   └── audit_log.py

├── schemas/
│   ├── __init__.py
│   ├── user.py            # Pydantic schemas for users
│   ├── broker.py
│   ├── listing.py
│   ├── vehicle.py
│   ├── property.py
│   ├── payment.py
│   ├── chat.py
│   ├── notification.py
│   ├── verification.py
│   ├── analytics.py
│   └── common.py          # Shared schema patterns

├── services/
│   ├── __init__.py
│   ├── auth_service.py
│   ├── user_service.py
│   ├── broker_service.py
│   ├── listing_service.py
│   ├── vehicle_service.py
│   ├── property_service.py
│   ├── payment_service.py
│   ├── chat_service.py
│   ├── notification_service.py
│   ├── verification_service.py
│   ├── analytics_service.py
│   └── file_service.py

├── api/
│   └── v1/
│       ├── __init__.py
│       ├── endpoints/
│       │   ├── __init__.py
│       │   ├── auth.py
│       │   ├── users.py
│       │   ├── brokers.py
│       │   ├── listings.py
│       │   ├── vehicles.py
│       │   ├── properties.py
│       │   ├── uploads.py
│       │   ├── payments.py
│       │   ├── verification.py
│       │   ├── chat.py
│       │   ├── analytics.py
│       │   ├── notifications.py
│       │   ├── admin.py
│       │   └── healthcheck.py
│       └── router.py       # Combines all endpoint routers

├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_users.py
│   ├── test_listings.py
│   └── conftest.py

├── scripts/
│   ├── __init__.py
│   ├── seed_data.py
│   ├── backup_db.py
│   └── maintenance.py

├── .env
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
└── README.md
```

## 📘 2. Module-Level Documentation

---

## app/core/

Core application logic & configuration:

- **config.py** – loads `.env` and sets environment variables (DB URL, Redis, secret keys)  
- **database.py** – SQLAlchemy engine & Base  
- **security.py** – password hashing & token validation  
- **jwt.py** – JWT token creation & verification  
- **auth_backend.py** – OAuth2PasswordBearer + JWT middleware  
- **caching.py** – Redis initialization & decorators  
- **payments.py** – third-party payment handling (Stripe, Telebirr, etc.)  
- **tasks.py** – Celery async tasks (email sending, verification)  
- **logging_config.py** – structured logging (console & file)  
- **utils.py** – helper functions (UUID generation, validators, file helpers)  
- **middleware.py** – custom FastAPI middlewares (CORS, logging, error handling)  

---

## app/db/

Database abstraction & initialization:

- **session.py** – provides `get_db()` dependency for FastAPI routes  
- **base_class.py** – SQLAlchemy Base class for models  
- **init_db.py** – seed initial admin/test data  
- **migrations/** – Alembic migration files for schema changes  

---

## app/models/

SQLAlchemy ORM models:

- One model per file (user.py, payment.py, listing.py, etc.)  
- Includes relationships, constraints, indexing, and timestamps  

---

## app/schemas/

Pydantic models for request/response validation:

- Base, Create, Update, and Response classes per entity  
- Mirrors the structure of `app/models/` for consistency  

---

## app/services/

Business logic connecting models & APIs:

- Handles orchestration between database models and endpoints  
- Example: `payment_service.py` → validate transaction → save record → trigger webhook  

---

## app/api/v1/endpoints/

FastAPI route handlers per entity:

- Each file corresponds to a resource (users, payments, listings, etc.)  
- Uses `APIRouter` for modular route inclusion  
- Handles authentication dependencies and Pydantic schema validation  

---

## app/tests/

Pytest test cases:

- Mock database, authentication, and data flow  
- Test endpoints, services, and business logic thoroughly
## 🧩 3. Build Roadmap (Priority & Dependencies)

| Priority   | Phase | Component                                     | Dependencies      | Description                             |
|-----------|-------|-----------------------------------------------|-----------------|-----------------------------------------|
| 🥇 High   | 1     | core/config.py, database.py, security.py     | none            | Setup environment, DB, and security     |
| 🥈 High   | 2     | models/, schemas/, db/base_class.py          | database        | Define DB models & schemas              |
| 🥈 High   | 3     | services/auth_service.py, api/v1/endpoints/auth.py | models, schemas | Authentication & JWT issuance           |
| 🥉 Medium | 4     | services/user_service.py, api/v1/endpoints/users.py | auth          | CRUD & profile management               |
| 🥉 Medium | 5     | listing_service.py, vehicle_service.py, property_service.py | user | Marketplace logic                        |
| 🥉 Medium | 6     | payment_service.py, core/payments.py        | listings        | Payment gateway integration             |
| ⚙️ Low    | 7     | chat_service.py, notification_service.py    | user            | Chat & notification modules             |
| ⚙️ Low    | 8     | analytics_service.py, verification_service.py | core           | Insights & KYC verification             |
| 🧾 Ongoing | 9    | logging_config.py, middleware.py             | all             | Monitoring & middleware improvements    |
| 🧪 Final  | 10    | tests/, docker-compose.yml                    | all             | Testing & containerization              |

## 🚀 4. Recommended Tech Stack

| Layer            | Tool                     |
|-----------------|--------------------------|
| Framework        | FastAPI                  |
| ORM              | SQLAlchemy + Alembic     |
| Database         | PostgreSQL               |
| Caching          | Redis                    |
| Async Tasks      | Celery                   |
| Auth             | OAuth2 + JWT             |
| Storage          | AWS S3 / Google Cloud    |
| Testing          | Pytest                   |
| Containerization | Docker                   |
| Deployment       | Nginx + Gunicorn         |
| CI/CD            | GitHub Actions           |

## 📋 5. To-Do / Deliverables & Schedule

| Phase | Deliverable                                     | Owner       | Estimated Timeline |
|-------|------------------------------------------------|------------|-----------------|
| 1     | Initialize FastAPI app & main.py               | Backend Dev | Week 1          |
| 1     | Setup core/config, security, jwt               | Backend Dev | Week 1          |
| 2     | Create models & schemas (User, Broker, Listing)| Backend Dev | Week 2          |
| 2     | Setup DB migrations & seed data                | Backend Dev | Week 2          |
| 3     | Implement Auth service & endpoints             | Backend Dev | Week 3          |
| 3     | Implement User CRUD service & endpoints        | Backend Dev | Week 3          |
| 4     | Implement Listing, Vehicle, Property services | Backend Dev | Week 4          |
| 4     | Integrate Payment gateway service              | Backend Dev | Week 4          |
| 5     | Add Chat & Notification modules                | Backend Dev | Week 5          |
| 5     | Add Caching & Analytics modules                | Backend Dev | Week 5          |
| 6     | Logging, Middleware, Error Handling            | Backend Dev | Week 6          |
| 6     | Write Tests & achieve Pytest coverage          | QA / Dev    | Week 6          |
| 7     | Docker setup & containerization                | DevOps      | Week 6          |
| 7     | Deployment to staging/production               | DevOps      | Week 7          |


# 📋 Full Deliverables / Tasks for Implementation

This table outlines **each file/folder** in the project, what it is responsible for, and what needs to be implemented. It is written to be clear for beginners.

| File / Folder                        | Description / Deliverable                                                                 | Notes / Implementation Details |
|-------------------------------------|-------------------------------------------------------------------------------------------|--------------------------------|
| `app/__init__.py`                    | Package initialization                                                                    | Leave empty, just `__init__.py` to make `app` a Python package |
| `app/main.py`                        | FastAPI app entrypoint                                                                    | Create FastAPI instance, include router, setup middleware |
| **app/core/**                        | Core application logic                                                                    | Handles config, security, JWT, caching, payments, etc. |
| `core/__init__.py`                   | Package initialization                                                                    | Empty file |
| `core/config.py`                      | Global settings & environment variables                                                  | Load `.env`, define DB URL, Redis, secret keys |
| `core/database.py`                    | SQLAlchemy engine & Base                                                                 | Setup DB engine, sessionmaker, Base declarative |
| `core/security.py`                    | Password hashing & token utilities                                                      | Implement bcrypt hashing & verification functions |
| `core/jwt.py`                         | JWT encode/decode logic                                                                  | Generate JWT, decode, check expiry |
| `core/auth_backend.py`                | OAuth2/JWT integration                                                                   | Implement FastAPI dependency for OAuth2PasswordBearer |
| `core/caching.py`                     | Redis cache setup & utilities                                                           | Connect to Redis, provide decorator for caching results |
| `core/payments.py`                    | Payment gateway integrations                                                            | Implement Stripe / Telebirr integration functions |
| `core/tasks.py`                       | Celery async tasks                                                                       | Setup Celery, example tasks like sending email, verification |
| `core/logging_config.py`              | Logging setup & formatters                                                              | Configure logging format (JSON or plain), file & console |
| `core/utils.py`                       | Helper functions                                                                         | UUID generation, file validators, common utilities |
| `core/middleware.py`                  | Request/response middlewares                                                            | Custom middlewares (CORS, logging, error handling) |
| **app/db/**                           | Database abstraction & initialization                                                   | Manages sessions, migrations, initial data |
| `db/__init__.py`                      | Package initialization                                                                    | Empty file |
| `db/session.py`                       | DB session management                                                                    | Create `get_db()` dependency for FastAPI routes |
| `db/base_class.py`                    | Declarative Base for SQLAlchemy models                                                 | Base class for all models |
| `db/init_db.py`                        | Seed / initial data creation                                                            | Create admin/test data |
| `db/migrations/`                      | Alembic migration folder                                                                | Alembic scripts for schema changes |
| **app/models/**                       | SQLAlchemy ORM models                                                                   | Each file represents a table/entity |
| `models/__init__.py`                  | Package initialization                                                                    | Empty file |
| `models/user.py`                       | User table/model                                                                        | Columns: id, name, email, hashed_password, timestamps |
| `models/broker.py`                     | Broker table/model                                                                      | Columns: id, name, contact, license info |
| `models/listing.py`                    | Generic listing table                                                                    | Columns: id, title, description, type, owner_id |
| `models/vehicle.py`                    | Vehicle listing table                                                                    | Columns: id, model, brand, year, listing_id |
| `models/property.py`                   | Property listing table                                                                   | Columns: id, address, size, listing_id |
| `models/payment.py`                    | Payments & transactions                                                                  | Columns: id, user_id, amount, status, gateway, timestamps |
| `models/chat.py`                       | Chat sessions/messages                                                                   | Columns: id, sender_id, receiver_id, message, timestamps |
| `models/notification.py`               | Push/email notifications                                                                | Columns: id, user_id, type, content, status |
| `models/verification.py`               | KYC / Document verification                                                             | Columns: id, user_id, document_type, status |
| `models/analytics.py`                  | Analytics & metrics data                                                                | Columns: id, entity, metric_name, value, timestamps |
| `models/audit_log.py`                  | System event audit trails                                                               | Columns: id, action, user_id, timestamps |
| **app/schemas/**                        | Pydantic models for request/response validation                                         | Mirrors models for API input/output |
| `schemas/__init__.py`                  | Package initialization                                                                    | Empty file |
| `schemas/user.py`                      | User schemas                                                                            | Base, Create, Update, Response classes |
| `schemas/broker.py`                    | Broker schemas                                                                          | Base, Create, Update, Response classes |
| `schemas/listing.py`                   | Listing schemas                                                                          | Base, Create, Update, Response classes |
| `schemas/vehicle.py`                   | Vehicle schemas                                                                          | Base, Create, Update, Response classes |
| `schemas/property.py`                  | Property schemas                                                                         | Base, Create, Update, Response classes |
| `schemas/payment.py`                   | Payment schemas                                                                          | Base, Create, Update, Response classes |
| `schemas/chat.py`                      | Chat schemas                                                                             | Base, Create, Update, Response classes |
| `schemas/notification.py`              | Notification schemas                                                                     | Base, Create, Update, Response classes |
| `schemas/verification.py`              | Verification schemas                                                                     | Base, Create, Update, Response classes |
| `schemas/analytics.py`                 | Analytics schemas                                                                        | Base, Create, Update, Response classes |
| `schemas/common.py`                     | Shared schema patterns (pagination, response base)                                     | Reusable schema classes |
| **app/services/**                       | Business logic / orchestrating between models & APIs                                   | Core logic of the system |
| `services/__init__.py`                 | Package initialization                                                                    | Empty file |
| `services/auth_service.py`             | Auth logic (login, register, password reset)                                          | Validate login, hash password, JWT generation |
| `services/user_service.py`             | User CRUD & profiles                                                                    | Create, Read, Update, Delete users |
| `services/broker_service.py`           | Broker-specific business logic                                                         | Broker CRUD & validations |
| `services/listing_service.py`          | Listing CRUD & marketplace logic                                                      | Create/update listings, filtering, searching |
| `services/vehicle_service.py`          | Vehicle-specific logic                                                                 | CRUD, validation, linking to listing |
| `services/property_service.py`         | Property-specific logic                                                                | CRUD, validation, linking to listing |
| `services/payment_service.py`          | Payment transaction & webhook handling                                               | Integrate with gateway, save transactions, update status |
| `services/chat_service.py`             | Chat logic                                                                             | Send/receive messages, link to users |
| `services/notification_service.py`     | Notification logic                                                                     | Push/email notifications, status tracking |
| `services/verification_service.py`     | KYC / document verification logic                                                     | Submit documents, update verification status |
| `services/analytics_service.py`        | Data insights logic                                                                    | Record metrics, aggregate analytics |
| `services/file_service.py`             | File upload/download helpers                                                           | Upload to S3/Cloud, generate URLs, validate files |
| **app/api/v1/endpoints/**               | FastAPI route handlers                                                                | Grouped by entity, use APIRouter |
| `endpoints/__init__.py`                | Package initialization                                                                    | Empty file |
| `endpoints/auth.py`                     | Auth endpoints                                                                          | Login, register, token refresh |
| `endpoints/users.py`                    | User endpoints                                                                          | CRUD endpoints, profile routes |
| `endpoints/brokers.py`                  | Broker endpoints                                                                        | CRUD endpoints for brokers |
| `endpoints/listings.py`                 | Listing endpoints                                                                       | CRUD, search & filter listings |
| `endpoints/vehicles.py`                 | Vehicle endpoints                                                                       | CRUD endpoints, link to listings |
| `endpoints/properties.py`               | Property endpoints                                                                      | CRUD endpoints, link to listings |
| `endpoints/uploads.py`                  | File upload endpoints                                                                   | Upload documents, images, validate file types |
| `endpoints/payments.py`                 | Payment endpoints                                                                       | Trigger payment, webhook listener, status check |
| `endpoints/verification.py`            | Verification endpoints                                                                 | Upload docs, check status |
| `endpoints/chat.py`                     | Chat endpoints                                                                          | Send/receive messages, conversation list |
| `endpoints/analytics.py`               | Analytics endpoints                                                                     | Metrics retrieval, stats |
| `endpoints/notifications.py`           | Notification endpoints                                                                 | Push/email notification triggers |
| `endpoints/admin.py`                    | Admin-specific endpoints                                                                | User management, audit log, system settings |
| `endpoints/healthcheck.py`             | Health check endpoints                                                                  | API status, DB connection status |
| `router.py`                             | Combine all endpoint routers                                                            | Include all APIRouters in main FastAPI app |
| **app/tests/**                          | Test cases                                                                               | Use pytest for endpoints & services |
| `test_auth.py`                          | Test auth endpoints & services                                                          | Login, register, JWT validation |
| `test_users.py`                         | Test user endpoints & services                                                         | CRUD & profile operations |
| `test_listings.py`                      | Test listing endpoints & services                                                      | CRUD, search, filter |
| `conftest.py`                           | Pytest fixtures                                                                        | Mock DB session, test clients |
| **app/scripts/**                        | Helper scripts                                                                          | Seeding, backup, maintenance |
| `seed_data.py`                          | Initialize test data                                                                     | Create initial users, listings, brokers |
| `backup_db.py`                          | Backup database script                                                                  | Dump DB to file |
| `maintenance.py`                        | Maintenance script                                                                      | Clean old files, rotate logs |
| `.env`                                  | Environment variables                                                                   | DB URL, Redis, secret keys, gateway keys |
| `requirements.txt`                      | Python dependencies                                                                    | List all packages |
| `Dockerfile`                            | Containerization                                                                         | Build image for FastAPI app |
| `docker-compose.yml`                    | Compose services                                                                         | Define app, DB, Redis, Celery |
| `alembic.ini`                           | Alembic config                                                                           | Setup migration tool for DB |

# 📋 Task Assignment & Schedule for Two Developers

This table organizes the full project tasks, assigns them to **2 developers**, includes **deliverables**, **estimated duration**, **dependencies**, and **start/end weeks**.

| Task # | Phase | Task / Deliverable                                     | Owner        | Duration | Dependencies                            | Start Week | End Week |
|--------|-------|--------------------------------------------------------|-------------|----------|----------------------------------------|------------|----------|
| 1      | Setup | Initialize FastAPI app & `main.py`                     | Dev 1       | 1 week   | None                                    | 1          | 1        |
| 2      | Setup | Setup core/config, security, jwt                       | Dev 2       | 1 week   | None                                    | 1          | 1        |
| 3      | Setup | Configure DB engine & session (`core/database.py`)     | Dev 1       | 1 week   | Task 1,2                                | 1          | 1        |
| 4      | Setup | Configure logging & middleware (`core/logging_config.py`, `middleware.py`) | Dev 2 | 1 week | Task 2                                   | 1          | 1        |
| 5      | Core Entities | Create models & schemas (`user`, `broker`, `listing`) | Dev 1 | 1 week | Task 3                                   | 2          | 2        |
| 6      | Core Entities | Create remaining models & schemas (`vehicle`, `property`, `payment`, `chat`, `notification`, `verification`, `analytics`, `audit_log`) | Dev 2 | 1 week | Task 3                                   | 2          | 2        |
| 7      | Core Entities | Setup DB migrations & initial seed (`db/migrations`, `init_db.py`) | Dev 1 | 1 week | Task 5,6                                | 3          | 3        |
| 8      | Auth | Implement Auth service & endpoints (`auth_service.py`, `endpoints/auth.py`) | Dev 2 | 1 week | Task 5,6                                | 3          | 3        |
| 9      | User | Implement User CRUD service & endpoints (`user_service.py`, `endpoints/users.py`) | Dev 1 | 1 week | Task 5                                   | 3          | 3        |
| 10     | Marketplace | Implement Listing, Vehicle, Property services (`listing_service.py`, `vehicle_service.py`, `property_service.py`) | Dev 2 | 1 week | Task 6                                   | 4          | 4        |
| 11     | Payments | Integrate Payment gateway (`payment_service.py`, `core/payments.py`, `endpoints/payments.py`) | Dev 1 | 1 week | Task 10                                  | 4          | 4        |
| 12     | Enhancements | Add Chat & Notification modules (`chat_service.py`, `notification_service.py`, endpoints) | Dev 2 | 1 week | Task 6,10                                | 5          | 5        |
| 13     | Enhancements | Add Caching & Analytics modules (`caching.py`, `analytics_service.py`, endpoints) | Dev 1 | 1 week | Task 6,10                                | 5          | 5        |
| 14     | Stability | Logging, Middleware, Error Handling updates         | Dev 2       | 1 week   | Task 4                                   | 6          | 6        |
| 15     | Testing | Write Pytest tests for auth, user, listings          | Dev 1       | 1 week   | Task 8,9,10                              | 6          | 6        |
| 16     | Testing | Write remaining tests & achieve coverage             | Dev 2       | 1 week   | Task 12,13                               | 6          | 6        |
| 17     | DevOps | Docker setup & containerization                       | Dev 1       | 1 week   | Task 1-16                                | 6          | 6        |
| 18     | DevOps | Deployment to staging/production                      | Dev 2       | 1 week   | Task 17                                  | 7          | 7        |
