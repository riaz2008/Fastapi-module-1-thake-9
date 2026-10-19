from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
import models 
from models import Todos
from database import engine, SessionLocal
from typing import Annotated
from fastapi.responses import JSONResponse

app = FastAPI()

class Todo(BaseModel):
    id : int
    title : str 
    description : str = Field(max_length=100)
    priority : int = Field(gt=0, lt=6)
    completed : bool

models.Base.metadata.create_all(bind=engine)

def db_get():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(db_get)]    

@app.get('/')
def read_todos(db : db_dependency):
    return db.query(Todos).all()

@app.get('/todo/{todo_id}')
def read_specific_todos(db : db_dependency, todo_id : int):
    specific_todos = db.query(Todos).filter(Todos.id == todo_id).first()
    if specific_todos is not None:
        return specific_todos
    else:
        raise HTTPException(status_code = 404,detail = 'Todo not found')
    
@app.post('/create/')
def create_todos(db : db_dependency, new_todo : Todo):
    todo_model = Todos(**new_todo.model_dump())
    db.add(todo_model)
    db.commit()

    return JSONResponse(status_code=201, content={'message':'To do create successfully'})