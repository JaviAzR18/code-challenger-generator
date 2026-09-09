from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import challenges, webhooks

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(challenges.router, prefix="/api")
# app.include_router(webhooks.router, prefix="/webhooks")