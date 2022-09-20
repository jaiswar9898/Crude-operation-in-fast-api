
from email.policy import default
from http.client import HTTPException
from tkinter.tix import COLUMN, INTEGER
from tokenize import String
from typing import List
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import json
from database import Base,engine,SessionLocal
from sqlalchemy import Column,String,Integer,Boolean
from models import Users 
from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
# templates = Jinja2Templates(directory="templates")



Base.metadata.create_all(bind=engine) # It will create table and will bring in database 
app = FastAPI() # It will create fast api 


def get_db():
    db=SessionLocal()
    try:
        yield db 
    finally:
        db.close()

class UserSchema(BaseModel):
    name:str
    email:str
    password:str
    class Config:
        orm_mode=True   # it will help to convert the dictionary data in json format 

class UserCreateSchema(UserSchema):
    password:str
#Get method

@app.get("/users",response_model=List[UserSchema])
def get_users(db:Session=Depends(get_db)):
    return db.query(Users).all()

@app.post("/users",response_model=UserCreateSchema)
def get_users(user:UserCreateSchema,db:Session=Depends(get_db)):
    u=Users(name=user.name,email=user.email,password=user.password)
    db.add(u)
    db.commit() #db.commit will save the data 
    return u 

@app.put("/users/{user_id}",response_model=UserSchema)
def update_user(user_id:int,user:UserSchema,db:Session=Depends(get_db)):
    try:
       u=db.query(Users).filter(Users.id==user_id).first()
       u.name=user.name 
       u.email=user.email
       u.password=user.password
       db.add(u)
       db.commit()
       return u 
    except:
        return HTTPException(status_code=404,details="user not found")

@app.delete("/users/{user_id}",response_class=JSONResponse)
def delete_user(user_id:int,db:Session=Depends(get_db)):
    try:
        u=db.query(Users).filter(Users.id==user_id).first()
        db.delete(u)
        db.commit()
        return {f"user of id {user_id} has been declared":True}
    except:
        return HTTPException(status_code=404,detail="user not found")
