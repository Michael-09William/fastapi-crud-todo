from fastapi import FastAPI,HTTPException,Response,status
import uvicorn
from pydantic import BaseModel, Field 
import sqlite3

conn=sqlite3.connect("tasks.db",check_same_thread=False)
conn.row_factory=sqlite3.Row


cursor=conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL ,
done BOOLEAN DEFAULT 0)
    """)

cursor.execute("SELECT COUNT(*) FROM tasks")
count=cursor.fetchone()[0]

if count==0:
    sample_tasks=[
        ("DO Assignment 2",0),
        ("Learn Backend with sqLite",1),
        ("Learn RAG",0)
    ]
    cursor.executemany("INSERT INTO tasks(title,done) VALUES(?,?)",sample_tasks)
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
    cursor.execute("SELECT * FROM tasks")
    tasks=cursor.fetchall()
    return tasks


@app.get('/tasks/{TaskId}')
async def showing_spec_task(TaskId:int):
    """Retrieve a single task by its unique ID from database."""
    cursor.execute('SELECT * FROM tasks WHERE id=?',(TaskId,))
    task=cursor.fetchone()
    if task:
        return task
    else:
        raise HTTPException(status_code=404, detail=f"Task not found")

#Stage 3: Post A new Task

class CreateNewT(BaseModel):
    title:str 
    done: bool=False

@app.post('/tasks',status_code=status.HTTP_201_CREATED)
async def create_task(tasks:CreateNewT):
    """Create a new task and store it in SQLite database."""
    if not tasks.title or not tasks.title.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Title is required and cannot be empty")
    cursor.execute("INSERT INTO tasks(title,done) VALUES(?,?)",(tasks.title.strip(),int(tasks.done)))

    conn.commit()

    new_id=cursor.lastrowid

    cursor.execute("SELECT * FROM tasks WHERE id=?",(new_id,))

    create_task=cursor.fetchone()

    return create_task


#Stage 4 : Update and Delete

@app.put('/tasks/{id}')
async def update_id_title(id:int ,task_data:CreateNewT):
        """Update an existing task's title or status."""
        if not task_data.title or not task_data.title.strip():
               raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                   detail="Title is required and cannot be empty")

        cursor.execute("SELECT * FROM tasks WHERE id=?",(id,))
        task=cursor.fetchone()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found")
        
        cursor.execute("UPDATE tasks SET title=? , done=? WHERE id=?",(task_data.title.strip(),int(task_data.done),id))
        conn.commit()

        cursor.execute("SELECT * FROM tasks WHERE id=?",(id,))
        updated_task=cursor.fetchone()
        return updated_task


@app.delete('/tasks/{id}')
async def delete_tasks(id:int):
    """Delete a task from the database by ID."""
    cursor.execute("SELECT * FROM tasks WHERE id=?",(id,))
    task=cursor.fetchone()
    if not task:
         raise HTTPException(
                         status_code=status.HTTP_404_NOT_FOUND,
                         detail="Task not found")
         
   
    cursor.execute("DELETE FROM tasks WHERE id=?",(id,))
    conn.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

