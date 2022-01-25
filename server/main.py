from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from blob.routers import file_router
from blob.db.database import database

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins="*", allow_methods="*")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(file_router.router)
