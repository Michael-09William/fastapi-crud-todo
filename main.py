import os
from dotenv import load_dotenv
from fastapi import FastAPI,HTTPException,Response,status
import uvicorn
from pydantic import BaseModel, Field 
import psycopg
from psycopg.rows import dict_row
from database import init_db

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

conn=psycopg.connect(DATABASE_URL, row_factory=dict_row)
cursor=conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(id SERIAL PRIMARY KEY,
title TEXT NOT NULL ,
done BOOLEAN DEFAULT FALSE)
    """)

cursor.execute("SELECT COUNT(*) FROM tasks")
count=cursor.fetchone()['count']

if count==0:
    sample_tasks=[
        ("DO Assignment 2",False),
        ("Learn Backend with sqLite",True),
        ("Learn RAG",False)
    ]
    cursor.executemany("INSERT INTO tasks(title,done) VALUES(%s,%s);",sample_tasks)
    conn.commit()

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

    cursor.execute("SELECT * FROM tasks;")
    tasks=cursor.fetchall()
    return tasks


@app.get('/tasks/{TaskId}')
async def showing_spec_task(TaskId:int):
    """Retrieve a single task using parameterized query (%s)."""

    cursor.execute('SELECT * FROM tasks WHERE id=%s;',(TaskId,))
    task=cursor.fetchone()

    if task:
        return task
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

    cursor.execute("INSERT INTO tasks(title,done) VALUES(%s,%s) RETURNING *;",(tasks.title.strip(),tasks.done))

    new_task=cursor.fetchone()
    conn.commit()

    return new_task


#Stage 4 : Update and Delete

@app.put('/tasks/{id}')
async def update_id_title(id:int ,task_data:CreateNewT):
        """Update an existing task's title or status."""

        if not task_data.title or not task_data.title.strip():

               raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                   detail={"error": "Title is required and cannot be empty"})

        cursor.execute("SELECT * FROM tasks WHERE id=%s;",(id,))
        task=cursor.fetchone()

        if not task:
            raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail={"error": "Task not found"},
)
        
        cursor.execute("UPDATE tasks SET title=%s , done=%s WHERE id=%s RETURNING *;",(task_data.title.strip(),task_data.done,id))

        updated_task=cursor.fetchone()
        conn.commit()

        return updated_task
 

@app.delete('/tasks/{id}')
async def delete_tasks(id:int):
    """Delete a task from the database by ID."""

    cursor.execute("SELECT * FROM tasks WHERE id=%s;",(id,))
    task=cursor.fetchone()

    if not task:
         
         raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail={"error": "Task not found"},
)
         
   
    cursor.execute("DELETE FROM tasks WHERE id=%s;",(id,))
    conn.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

