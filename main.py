#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI
from fastapi import Body
from fastapi import Query, Path



app = FastAPI()

#Models
class Person(BaseModel):
    first_name:str 
    last_name:str
    age:int
    hair_color:Optional[str] = None
    is_married:Optional[bool] = None

class Location(BaseModel):
    city:str
    state:str
    transfer:str


@app.get("/") #Path Operation Decorator
def home(): #Path Operation Function
    return {"Hello": "World"}

#Request and Response Body
@app.post("/person/new") #Request Body
def create_person(person:Person = Body(...)):#Los tres puntos "..." significan que es obligatorio
    return person

#Validaciones : Query Parameters
#127.0.0.1:8000/person/detail?name=John&age=12
@app.get("/person/detail")
def show_person(
    name:Optional[str] = Query(
        default=None,
        min_length=1,
        max_length=20,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters"
        ), #opcional
    age:int = Query(
        ...,
        ge=5,
        le=150,
        title="Person Age",
        description="This is the person age. It's required"
        ) #Los tres puntos "..." significan que es obligatorio
):
    return {name:age}

#Validaciones : Path Parameters
#127.0.0.1:8000/person/detail/25
@app.get("/person/detail/{person_id}")
def show_person(
    person_id:int = Path(
        ...,
        gt=0,
        title="Person Id",
        description="This is the person Id. It's required"
        )
): 
    return {person_id: "it exists!"}

#validaciones : Request Body
#127.0.0.1:8000/person/25
@app.put("/person/{person_id}")
def update_person(
    person_id:int = Path(
        ...,
        title="Person Id",
        description="This is the person Id",
        gt=0
        ),
    person:Person = Body(...),
    Location:Location = Body(...)
):
    results = person.dict()
    results.update(Location.dict())
    return results