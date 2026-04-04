from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import classify, health, research, summarize

app = FastAPI(
    title="Principal Idea Backlog API",
    description="Transform rough ideas into structured, actionable output.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(summarize.router)
app.include_router(classify.router)
app.include_router(research.router)
