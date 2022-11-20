from fastapi import FastAPI

app = FastAPI()

@app.get("/") #Path Operation Decorator
def home(): #Path Operation Function
    return {"Hello": "World"}