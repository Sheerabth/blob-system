from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server_src.routers import file, auth, user

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins="*", allow_methods="*")

app.include_router(file.router, prefix="/file", tags=["file"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/user", tags=["user"])

