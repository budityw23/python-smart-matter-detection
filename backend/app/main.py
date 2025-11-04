from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager

from app.api.graphql.schema import schema
from app.utils.database import get_db
import os
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print("Starting up...")
    yield
    # Shutdown
    print("Shutting down...")


app = FastAPI(
    title="Smart Matter Opportunity Detector",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# GraphQL endpoint
async def get_context():
    """Provide context to GraphQL resolvers"""
    db_gen = get_db()
    db = await anext(db_gen)
    try:
        return {"db": db}
    finally:
        try:
            await anext(db_gen)
        except StopAsyncIteration:
            pass


graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,
)

app.include_router(graphql_app, prefix="/graphql")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "smart-matter-detector"
    }


@app.get("/")
async def root():
    return {"message": "Smart Matter Opportunity Detector API"}
