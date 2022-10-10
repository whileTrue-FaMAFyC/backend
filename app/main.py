from fastapi import FastAPI
from routers import match

app = FastAPI()

app.include_router(match.router)