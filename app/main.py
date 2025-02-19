from functools import lru_cache
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger
from app.routers import payment
from . import config


@lru_cache()
def get_settings():
    """
    Config settings function.
    """
    return config.Settings()


conf_settings = get_settings()

app = FastAPI(debug=conf_settings.debug)

app.add_middleware(CORSMiddleware)

app.include_router(payment.router)

logger.add("log_api.log", rotation="10 MB")  # Automatically rotate log file


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.exception(str(exc))
    return JSONResponse(
        status_code=500,
        content={"detail": "Database operation failed"},
    )


@app.get("/health")
def health():
    """
    Health router.
    """
    result = {
        "status": "ok"
    }
    return result
