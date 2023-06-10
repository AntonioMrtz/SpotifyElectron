from fastapi import FastAPI

app = FastAPI()

@app.get("/my-first-api/{name}")
def hello(name: str):
    text = 'Hello ' + name + '!'
    return text