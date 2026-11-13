from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def base_function():
    return {"status": "Running"}
