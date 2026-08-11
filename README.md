# 📝 Task API (FastAPI)

A simple, lightweight, in-memory CRUD API for managing a to-do list.

Built as part of the FlyRank Internship (Backend Track - Week 2, Assignment A1).

---

## 🚀 Features (Implemented & Upcoming)

- [x] **Stage 1:** Root API description & `/health` endpoint.
- [x] **Stage 2:** Read endpoints (List all tasks & get single task with 404 error handling).
- [x] **Stage 3:** Create tasks with input validation (Pydantic).
- [x] **Stage 4:** Full CRUD (Update & Delete endpoints).
- [x] **Stage 5:** Swagger UI Interactive Docs.

---

## ⚙️ Installation

1. Clone the repository

```bash
git clone https://github.com/Michael-09William/fastapi-crud-todo.git
cd fastapi-crud-todo
```

2. Activate the virtual environment (Windows)

```cmd
.\env\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run the server

```bash
uvicorn main:app --reload
```

---

## 💡 Server

The server will start locally at:

http://127.0.0.1:8000

---

## 🛣️ API Endpoints

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/` | API Information | 200 OK |
| GET | `/health` | Server Health Status | 200 OK |
| GET | `/tasks` | Reading All Tasks  | 200 OK |
| GET | `/tasks/{taskId}` | Reading Specific Task | 200 OK |
| POST | `/tasks` | Creating New Task | 200 OK |
| PULL | `/tasks/{id}` | Updating Task Titile And Status | 200 OK |
| DELETE | `/tasks/{id}` | Deleting A Task | 200 OK |


---

## 🧪 Sample Request

```bash
curl -i http://localhost:8000/health
```

### Example Response

```http
HTTP/1.1 200 OK
date: Wed, 15 Jul 2026 15:09:00 GMT
server: uvicorn
content-type: application/json

{"status":"ok"}
```

---

## 📸 Swagger UI Preview

Screenshot will be added in **Stage 5**.

Swagger URL:

http://127.0.0.1:8000/docs



# Task API - Database Integration (Assignment 2)

A FastAPI backend service upgraded from in-memory storage to persistent SQLite database storage (`tasks.db`).

## Features
- **SQLite Persistence**: All CRUD operations directly interact with `tasks.db`, ensuring data survives server restarts.
- **Parametrized Queries**: Safe SQL execution to prevent SQL injection vulnerabilities.
- **RESTful Endpoints**:
  - `GET /tasks`: Retrieve all tasks.
  - `GET /tasks/{id}`: Fetch a single task by ID.
  - `POST /tasks`: Create a new task.
  - `PUT /tasks/{id}`: Update an existing task's title or status.
  - `DELETE /tasks/{id}`: Delete a task by ID.

## Why SQLite?
- **Single File**: The entire database lives in a local file (`tasks.db`), avoiding external service dependencies.
- **Zero Setup**: No extra server installation, user creation, or complex database configuration needed.
- **Data Persistence**: Data survives server restarts seamlessly.

## Database Management
- **File Location**: `tasks.db` is automatically created in the root directory upon server initialization if it does not exist.
- **Git Ignore**: `tasks.db` is intentionally listed in `.gitignore` so every new clone starts with a fresh database setup without conflict.
- **Auto-Initialization**: Running the app creates the `tasks` table automatically and seeds it with 3 default tasks on the first run.

## How to Run the Project
To start the server, run the following single command:

```bash
uvicorn main:app --reload
```

# 📝 Task API (FastAPI + PostgreSQL)

A robust RESTful CRUD API built with **FastAPI** and **PostgreSQL** (`psycopg3`) for task management, featuring input validation, database seeding, and Docker support.

Built as part of the FlyRank Internship (Backend Track).

---

## 🚀 Features & Progression

- **Stage 1**: Root API metadata & `/health` endpoint.
- **Stage 2**: Read endpoints (`/tasks` & `/tasks/{id}` with 404 handling).
- **Stage 3**: Full CRUD operations directly connected to PostgreSQL (`RETURNING *` queries).
- **Validation**: Strict request validation using **Pydantic** models.
- **Persistence**: Switched from SQLite to persistent **PostgreSQL** using parameterized queries to prevent SQL injection.
- **Containerization**: Configured with Docker & PostgreSQL environment setup.

---

## ⚙️ Local Setup & Installation

1. **Clone the repository**
   ```bash
   git clone [https://github.com/Michael-09William/fastapi-crud-todo.git](https://github.com/Michael-09William/fastapi-crud-todo.git)
   cd fastapi-crud-todo

2. **Environment Configuration** 
  create `.env` file in the root directory.

3. **Environment Config For Public**
  create `.env.example` 
 
  ```bash
  cp .env.example .env
  ```

4. **Run PostgreSQL Container**
  ```bash
  docker run --name taskdb -e POSTGRES_PASSWORD=dev -e POSTGRES_DB=tasks -p 5433:5432 -v taskdata:/var/lib/postgresql/data -d postgres:16
  ```
5. **Run The Full Stack**
  ```bash
  docker compose up --build
  ```