from fastapi import FastAPI
from routes.users import router as user_router
from routes.tickets import router as ticket_router
from database import Base,engine
import models.user
import models.ticket

Base.metadata.create_all(bind=engine)


app = FastAPI()

@app.middleware("http")
def my_middleware(request: Request, call_next):
    print(f"{request.method} request to {request.url.path}")

    response =call_next(request)

    print(f"Finished {request.url.path}")

    return response

app.include_router(user_router, prefix="/users")
app.include_router(ticket_router, prefix="/tickets")

@app.get("/")
def home():
    return {"message": "Hello boss"}