from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api.routes.auth import router as auth_router
from app.exceptions.custom_exception import AppException

app = FastAPI()


@app.get("/")
def base_function():
    return {"status": "Running"}


app.include_router(auth_router)


@app.exception_handler(AppException)
def app_exception_handler(exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
