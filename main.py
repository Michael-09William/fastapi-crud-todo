import os
from dotenv import load_dotenv
from fastapi import FastAPI,HTTPException,Response,status,Request,Header ,Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
from pydantic import BaseModel, Field 
from typing import Optional
#import psycopg
#from psycopg.rows import dict_row
#from database import init_db
from supabase import create_client, Client

security = HTTPBearer()
load_dotenv()
#DATABASE_URL = os.getenv("DATABASE_URL")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
PORT = int(os.getenv("PORT", 8000))

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in the environment variables.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)



app=FastAPI(title='Task API',
            description='A simple in-memory CRUD API for managing tasks',
            version='1.0')

listoftasks=[{'id':1,"title":'Create APIS','done':True},
             {'id':2,"title":'Testing APIS','done':False},
             {'id':3,"title":'RAG Project','done':True}]

# Stage 1: Root & Health Endpoints

@app.get('/')
async def root():
    """Return basic API information."""
    return {'name':'Task API',
            'version':'1.0',
            'endpoints': ["/tasks"]}

@app.get('/health')
async def health():
    """Check the server health status."""
    return{"status": "ok"}


# Stage 2: Read List and Single Task

@app.get('/tasks')
async def showing_tasks():
    """List all available tasks in the database."""

    response = supabase.table("tasks").select("*").execute()
    tasks = response.data
    return tasks


@app.get('/tasks/{TaskId}')
async def showing_spec_task(TaskId:int):
    """Retrieve a single task using parameterized query (%s)."""

    response = supabase.table("tasks").select("*").eq("id", TaskId).execute()
    task = response.data

    if task:
        return task[0]
    else:
        raise HTTPException(status_code=404, detail={"error": f"Task not found"})

#Stage 3: Post A new Task

class CreateNewT(BaseModel):
    title:str 
    done: bool=False

@app.post('/tasks',status_code=status.HTTP_201_CREATED)
async def create_task(tasks:CreateNewT):
    """Create a new task and store it in PostgreSQL database."""

    if not tasks.title or not tasks.title.strip():

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail={"error": "Title is required and cannot be empty"})

    response = supabase.table("tasks").insert({
        "title": tasks.title.strip(),
        "done": tasks.done
    }).execute()

    return response.data[0]


#Stage 4 : Update and Delete

@app.put('/tasks/{id}')
async def update_id_title(id:int ,task_data:CreateNewT):
        """Update an existing task's title or status."""

        if not task_data.title or not task_data.title.strip():

               raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                   detail={"error": "Title is required and cannot be empty"})

        response = supabase.table("tasks").select("*").eq("id", id).execute()
        task = response.data

        if not task:
            raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail={"error": "Task not found"},
)
        
        updated_response = supabase.table("tasks").update({
            "title": task_data.title.strip(),
            "done": task_data.done
        }).eq("id", id).execute()

      

        return updated_response.data[0]


@app.delete('/tasks/{id}')
async def delete_tasks(id:int):
    """Delete a task from the database by ID."""

    response = supabase.table("tasks").select("*").eq("id", id).execute()
    task = response.data

    if not task:
         
         raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail={"error": "Task not found"},
)

    response = supabase.table("tasks").delete().eq("id", id).execute()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

class AuthSchema(BaseModel):
    email: Optional[str] =None
    password: Optional[str] =None

@app.post('/auth/signup',status_code=status.HTTP_201_CREATED)

async def signup(auth:AuthSchema):
    """Sign up a new user using Supabase authentication."""

    if not auth.email or not auth.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail={"error": "Email and password are required"})
    try:
        response = supabase.auth.sign_up({
            "email": auth.email,
            "password": auth.password
        })

        if not response.user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail={"error": "User registration failed"})

        return response.user
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail={"error": str(e)})

@app.post('/auth/login')
async def login(auth: AuthSchema):
    """Log in an existing user using Supabase authentication."""

    if not auth.email or not auth.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail={"error": "Email and password are required"})

    try:
        response = supabase.auth.sign_in_with_password({
            "email": auth.email,
            "password": auth.password
        })

        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "token_type": "bearer"
        }
    
    except HTTPException:
            raise 
    except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail={"error": "Invalid login credentials"})

@app.get('/public/info', status_code=status.HTTP_200_OK)
async def public_info():

     return {"message": "Welcome stranger! This info is public."}



@app.get('/protected/profile')
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Extract and validate the current user from the Bearer token."""
    token = credentials.credentials.strip()

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Access token required"}
        )

    try:
        user_response = supabase.auth.get_user(jwt=token)
        if not user_response or not getattr(user_response, 'user', None):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": "Invalid or expired token"}
            )
        return user_response.user

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid or expired token"}
        )

    
# 2. Protected Routes 
@app.get('/protected/profile')
async def protected_profile(current_user = Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "created_at": str(getattr(current_user, 'created_at', ''))
    }

@app.get('/protected/dashboard')
async def protected_dashboard(current_user = Depends(get_current_user)):
    return {
        "message": f"Welcome to your dashboard, {current_user.email}!",
        "user_id": str(current_user.id)
    }

# 3. Logout Route
@app.post('/auth/logout', status_code=status.HTTP_204_NO_CONTENT)
async def logout(current_user = Depends(get_current_user)):
    try:
        supabase.auth.sign_out()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": str(e)}
        )