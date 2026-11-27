from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.routes.auth import router as auth_router
from app.api.routes.category import router as category_router
from app.api.routes.product import router as product_router
from app.api.routes.profile import router as profile_router
from app.exceptions.custom_exception import AppException

app = FastAPI()


@app.get("/")
def base_function():
    return {"status": "Running"}


app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(category_router)
app.include_router(product_router)


@app.exception_handler(AppException)
def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers,
    )
