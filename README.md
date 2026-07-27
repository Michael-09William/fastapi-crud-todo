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

## SQL Exploration (Stage 4)
Ran raw SQL directly via **DB Browser for SQLite**:
```sql
SELECT COUNT(*) FROM tasks;
```
Result: Returned the total number of tasks currently stored in the database, verifying that both FastAPI and external SQLite viewers share the exact same source of truth in real-time.