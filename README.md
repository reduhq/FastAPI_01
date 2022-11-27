# FastAPI - Aprendiendo FastAPI con Platzi
## Contenido:
* [Creando Entorno Virtual](#creando-nuestro-entorno-virtual-e-instalando-fastapi)
* [Tipos de datos especiales](#tipos-de-datos-especiales-en-fastapi)
* [Entradas de datos](#entradas-de-datos-en-fastapi)
    * [Path Parameters](#path-parameters)
    * [Query Parameters](#query-parameters)
    * [Request Body](#request-body)
    * [Formularios](#Formularios)
    * [Headers](#headers-y-cookies)
    * [Cookies](#headers-y-cookies)
    * [Files](#files)

>NOTA: Para ejecutar nuestra API en local, tenemos que usar el siguiente comando
>```sh
>uvicorn main:app --reload
>```

## Creando nuestro entorno virtual e instalando FastAPI
1. Creando nuestro entorno virtual
```sh
python3 -m venv venv
```
2. Activando nuestro entorno virtual
```sh
source venv/bin/activate
```
3. Instalando [FastAPI](https://fastapi.tiangolo.com/) y [Uvicorn](https://www.uvicorn.org/)
```sh
pip install fastapi uvicorn
```
4. Creando un requirements.txt
```sh
pip freeze > requirements.txt
```
5. Para instalar los paquetes de requirements.txt ejecutar este comando
```sh
pip install -r requirements.txt
```

## Tipos de datos especiales en FastAPI
* Enum
* HttpUrl
* FilePath
* DirectoryPath
* EmailStr `pip install pydantic[email]`
* PaymentCardNumber
* IpvAnyAdress
* NegativeFloat
* PositiveFloat
* NegativeInt
* PositiveInt

Puedes encontrar mas tipos de datos en [Pydantic Field Types](https://pydantic-docs.helpmanual.io/usage/types/#pydantic-types)


## Entradas de datos en FastAPI

|Tipos de entrada de datos| Descripción |
| ------------------ |:-------------:|
| [Path Parameters](#path-parameters)    |Son esos parametros obligatorios que se mandan mediante la url |
| [Query Parameters](#query-parameters)   |Son los parametros opcionales que pasamos mediante la url|
| [Request Body](#request-body)       |Son los archivos en formato JSON que nos envia un cliente a nuestra API|
| [Formularios](#Formularios)        |Son aquellos campos que tenemos en los formularios del frontend de una aplicacion que nos trae esos datos (mediante este metodo) a nuestra API|
| [Headers](#headers-y-cookies)            |Son cabeceras HTTP que pueden venir de cliente a servidor y viceversa|
| [Cookies](#headers-y-cookies)            |Son pequeños bloques de codigo y/o de datos que un servidor instala en nuestra computadora para poder trackear nuestra informacion a través de la web|
| [Files](#files)              |Es la entrada de datos que se refiere a los archivos dentro de FastAPI (Imagenes, Videos, etc), este tipo de entrada depende de dos clases (File y UploadFile)|

### Path Parameters
```python
# 127.0.0.1:8000/person/detail/25
@app.get("/person/detail/{person_id}")
def show_person(person_id:int = Path(...)): 
    return {person_id: "it exists!"}
```

### Query Parameters
```python
# 127.0.0.1:8000/person/detail?name=John&age=12
@app.get("/person/detail")
def show_person(
    name:Optional[str] = Query(None), #opcional
    age:int = Query(...) #obligatorio
):
    return {name:age}
```

### Request Body
```python
# 127.0.0.1:8000/person/25
@app.put("/person/{person_id}")
def update_person(
    person_id:int = Path(...),
    person:Person = Body(...),
    Location:Location = Body(...)
):
    results = person.dict()
    results.update(Location.dict())
    return results
```

### Formularios
Para trabajar con formularios se tiene que descargar el siguiente paquete:
```sh
pip install python-multipart
```
```python
# Ejemplo usando la entrada de dato tipo Formulario
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(username:str = Form(...), password:str = Form(...)):
    return LoginOut(username=username)
```

### Headers y Cookies
```py
# Trabajando con Cookies y Headers Parameters
@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK
)
def contact(
    first_name:str = Form(...),
    last_name:str = Form(...),
    email:EmailStr = Form(...),
    message:str = Form(...),
    user_agent:Optional[str] = Header(default=None),
    ads:Optional[str] = Cookie(default=None)
):
    return user_agent
```

### Files
```py
@app.post("/post-image")
def post_image(image:UploadFile = File(...)):
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2),
    }
```
