from fastapi import FastAPI
from endpoints import matching


app = FastAPI()
app.include_router(matching.router, prefix="/matching")
