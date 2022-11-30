#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException # para los status 400
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File



app = FastAPI()

#Models
class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class BasePerson(BaseModel):
    first_name:str = Field(
        ...,
        min_length=1,
        max_length=25,
        # example="Rey Eduardo"
        ) 
    last_name:str = Field(
        ...,
        min_length=1,
        max_length=25,
        # example="Halsall Quintero"
        )
    age:int = Field(
        ...,
        gt=0,
        le=115,
        # example=20
        )
    hair_color:Optional[HairColor] = Field(default=None)
    is_married:Optional[bool] = Field(default=None)

class Person(BasePerson):
    password:str = Field(..., min_length=8)

    class Config:
        schema_extra = {
            "example" : {
                "first_name": "Rey",
                "last_name": "Halsall",
                "age": 19,
                "hair_color": "black",
                "is_married": False,
                "password": "123456789"
            }
        }

class Location(BaseModel):
    city:str
    state:str
    country:str

    class Config:
        schema_extra = {
            "example" : {
                "city": "Bo. Omar Torrijos",
                "state": "Managua",
                "country": "Nicaragua"
            }
        }

class LoginOut(BaseModel):
    username:str = Field(..., max_length=20, example="reduhq")
    message:str = Field(default="Login Succesfully!")


@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    tags=["Home"]
    ) #Path Operation Decorator
def home(): #Path Operation Function
    return {"Hello": "World"}

#Request and Response Body
@app.post(
    path="/person/new",
    response_model=BasePerson,
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"],
    summary="Create Person in the app"
    ) #Request Body
def create_person(person:Person = Body(...)):
    """
    Create Person
    
    This path operation creates a new person in the app and save the information in the database
    
    Parameters:
    - Request body parameter:
        - **person: Person** -> A person model with first name, last name, age, hair color and marital status
        
    Returns a person model with first name, last name, age, hair color and marital status
    """
    return person

#Validaciones : Query Parameters
#127.0.0.1:8000/person/detail?name=John&age=12
@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    deprecated= True
    )
def show_person(
    name:Optional[str] = Query(
        default=None,
        min_length=1,
        max_length=20,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters",
        example="Rey"
        ), #opcional
    age:int = Query(
        ...,
        ge=5,
        le=150,
        title="Person Age",
        description="This is the person age. It's required",
        example=19
        ) #Los tres puntos "..." significan que es obligatorio
):
    """
    Show person

    This path operation shows a person who has a certain name and age given in the query 

    Parameters:
    - Query parameters:
        - **name: str** -> The person's name
        - **age: int** -> The person's age

    Returns a person who has the name and the age given ih the query
    """
    return {name:age}

#Validaciones : Path Parameters
#127.0.0.1:8000/person/detail/25
persons = [1, 2, 3, 4, 5]
@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
    )
def show_person(
    person_id:int = Path(
        ...,
        gt=0,
        title="Person Id",
        description="This is the person Id. It's required",
        example=25
        )
): 
    """
    Show person

    this path parameter shows if a person with a certain id exists or not

    Parameters:
    - Path parameters:
        - **Person_Id: int** -> The person's id

    Returns if a person with a certain id exists or not
    """
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person doesn't exist"
        )
    return {person_id: "it exists!"}

#validaciones : Request Body
#127.0.0.1:8000/person/25
@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Persons"]
    )
def update_person(
    person_id:int = Path(
        ...,
        title="Person Id",
        description="This is the person Id",
        gt=0,
        example=10
        ),
    person:Person = Body(...),
    Location:Location = Body(...)
):
    """
    Update a person

    This path parameter updates a person's information

    Parameters:
    - Path parameters:
        - **Person_id: int** -> The person's id
    - Body parameters:
        - **person: Person** -> A person model with first name, last name, age, hair color and marital status
        - **location: Location** -> a Location model with city, state, country

    Returns a JSON with the data uploaded in the person who has the id given in the query
    """
    results = person.dict()
    results.update(Location.dict())
    return results

# Datos dados desde Formularios
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
)
def login(username:str = Form(...), password:str = Form(...)):
    return LoginOut(username=username)

# Trabajando con Cookies y Headers Parameters
@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["Contact"]
)
def contact(
    first_name:str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    last_name:str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email:EmailStr = Form(...),
    message:str = Form(
        ...,
        min_length=20,
    ),
    user_agent:Optional[str] = Header(default=None),
    ads:Optional[str] = Cookie(default=None)
):
    return user_agent

# Trabajando con Files
@app.post(
    path="/post-image",
    tags=["Images"]
)
def post_image(
    image:UploadFile = File(...)
):
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2),
    }