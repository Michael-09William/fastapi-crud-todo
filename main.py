import os
from dotenv import load_dotenv
from fastapi import FastAPI,HTTPException,Response,status
import uvicorn
from pydantic import BaseModel, Field 
#import psycopg
#from psycopg.rows import dict_row
#from database import init_db
from supabase import create_client, Client

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

