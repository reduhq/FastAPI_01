#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI
from fastapi import Body
from fastapi import Query



app = FastAPI()

#Models
class Person(BaseModel):
    first_name:str 
    last_name:str
    age:int
    hair_color:Optional[str] = None
    is_married:Optional[bool] = None

@app.get("/") #Path Operation Decorator
def home(): #Path Operation Function
    return {"Hello": "World"}

#Request and Response Body
@app.post("/person/new") #Request Body
def create_person(person:Person = Body(...)):#Los tres puntos "..." significan que es obligatorio
    return person

#Validaciones : Query Parameters
@app.get("/person/detail")
def show_person(
    name:Optional[str] = Query(default=None, min_length=1, max_length=20), #opcional
    age:int = Query(..., ge=5, le=150) #Los tres puntos "..." significan que es obligatorio
):
    return {name:age}