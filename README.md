# FastAPI - Aprendiendo FastAPI con Platzi
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
4. Para instalar los paquetes de requirements.txt ejecutar este comando
```sh
pip install -r requirements.txt
```

> NOTA: Para ejecutar nuestra API en local, tenemos que usar el siguiente comando
> ```sh
> uvicorn main:app --reload
>```

## Formularios
Para trabajar con formularios se tiene que descargar el siguiente paquete:
```sh
pip install python-multipart
```

## Validando Email
Para validar un email necesitas descargar el siguiente paquete:
```sh
pip install pydantic[email]
```
