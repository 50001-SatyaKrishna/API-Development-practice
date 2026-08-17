from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import post,user,auth,vote
from  .config import settings

#print(settings.database_username)

app = FastAPI()

origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(vote.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Hello! Welcome to my world!"}

