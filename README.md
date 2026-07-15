## 📝 Task API (FastAPI)A simple, lightweight, in-memory CRUD API for managing a to-do list. Built as part of the FlyRank Internship (Backend Track - Week 2, Assignment A1).

### 🚀 Features (Implemented & Upcoming)[x] 
**Stage 1**: Root API description & /health endpoint.[ ] 
**Stage 2**: Read endpoints (List all tasks & get single task with 404 error handling).[ ] 
**Stage 3**: Create tasks with input validation (Pydantic).[ ] 
**Stage 4**: Full CRUD (Update and Delete endpoints).[ ] 
**Stage 5**: Swagger UI Interactive Docs.🛠️ Installation & How to RunFollow these steps to run the project locally:

1. Clone the repository:git clone https://github.com/Michael-09William/fastapi-crud-todo.git
cd fastapi-crud-todo
2. Activate your virtual environment (env):# On Windows (using CMD/Cmder):
.\env\Scripts\activate
3. Install dependencies:pip install -r requirements.txt
4. Start the FastAPI server:uvicorn main:app --reload

#### 💡 The server will start running locally on http://127.0.0.1:8000🛣️ API EndpointsMethodEndpointDescriptionStatus CodeGET/API Information (Root)200 OKGET/healthServer Health Status200 OK🧪 Sample Request & ResponseTesting the Health check endpoint via curl:curl -i http://localhost:8000/health

**Output**:HTTP/1.1 200 OK
**date**: Wed, 15 Jul 2026 15:09:00 GMT
**server**: uvicorn
**content-length**: 15
**content-type**: application/json

#### {"status":"ok"}
#### 📸 Swagger UI Preview(Screenshot will be added in Stage 5 at http://127.0.0.1:8000/docs)