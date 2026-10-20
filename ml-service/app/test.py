from fastapi import FastAPI

app = FastAPI()

@app.get("/ask/{query}")
def home(query : str):
    return {"message":"Hello World!"}