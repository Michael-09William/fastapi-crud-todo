from fastapi import FastAPI,HTTPException,Response,status
import uvicorn
from pydantic import BaseModel, Field 

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
    """List all available tasks in the list."""
    return listoftasks


@app.get('/tasks/{TaskId}')
async def showing_spec_task(TaskId:int):
    """Retrieve a single task by its unique ID."""
    for task in listoftasks:
        if task['id']==TaskId:
            return task 
        
    raise HTTPException(status_code=404, detail=f"Task {TaskId} not found")

#Stage 3: Post A new Task

class CreateNewT(BaseModel):
    title:str 
    done: bool

@app.post('/tasks',status_code=status.HTTP_201_CREATED)
async def create_task(tasks:CreateNewT):
    """Create a new task with in-memory persistence."""
    if listoftasks:
        new_id = listoftasks[-1]['id'] + 1
    # in case list is empty 
    else:
        new_id=1
    new_task={
        'id':new_id,
        'title':tasks.title.strip(),
        'done':False}
    
    listoftasks.append(new_task)

    return new_task

#Stage 4 : Update and Delete

@app.put('/tasks/{id}')
async def update_id_title(id:int ,task_data:CreateNewT):
        """Update an existing task's title or status."""
        for tasks in listoftasks:
            if tasks['id']== id:
                tasks['title']=task_data.title.strip()
                tasks['done']= task_data.done
            
                return tasks 
            
        raise HTTPException(status_code=404, detail=f"Task {id} not found")

@app.delete('/tasks/{id}')
async def delete_tasks(id:int):
    """Delete a task from the list by ID."""
    for tasks in listoftasks:
        if tasks['id']==id:
            listoftasks.remove(tasks)    
            return Response(status_code=status.HTTP_204_NO_CONTENT)
   
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Task with id {id} not found"
    )
