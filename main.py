from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel, Field

app=FastAPI(title='Task API',
            description='A simple in-memory CRUD API for managing tasks',
            version='1.0')



# Stage 1: Root & Health Endpoints

@app.get('/')
async def root():
    return {'name':'Task API',
            'version':'1.0',
            'endpoints': ["/tasks"]}

@app.get('/health')
async def health():
    return{"status": "ok"}