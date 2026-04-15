from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from routes.users import router as user_router
from routes.tickets import router as ticket_router
from database import Base, engine
import models.user
import models.ticket

from utils.logger import setup_logger
from utils.logger import get_logger
setup_logger()



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

logger=get_logger(__name__)

@app.middleware("http")
async def middleware(request: Request, call_next):
    logger.info(f"{request.method} request to {request.url.path}")

    response = await call_next(request)  

    logger.info(f"Finished {request.url.path}")

    return response


@app.middleware("http")
async def my_middleware(request: Request, call_next):
    print(f"{request.method} request to {request.url.path}")

    response = await call_next(request)  

    print(f"Finished {request.url.path}")

    return response


app.include_router(user_router, prefix="/users")
app.include_router(ticket_router, prefix="/tickets")

@app.get("/")
async def home():
    return {"message": "Hello boss"}