from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager
import logging

from app.api.graphql.schema import schema
from app.utils.database import get_db
from app.websocket.manager import manager as websocket_manager
import os
from dotenv import load_dotenv

load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info("🚀 Starting up Smart Matter Opportunity Detector...")
    yield
    logger.info("👋 Shutting down...")


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


# GraphQL endpoint with WebSocket manager in context
async def get_context():
    """Provide context to GraphQL resolvers"""
    db_gen = get_db()
    db = await anext(db_gen)
    try:
        return {
            "db": db,
            "websocket_manager": websocket_manager
        }
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


# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time notifications"""
    await websocket_manager.connect(websocket)

    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            logger.debug(f"Received from client: {data}")

            # Send ping/pong to keep connection alive
            if data == "ping":
                await websocket.send_text("pong")

    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
        logger.info("Client disconnected from WebSocket")

    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        websocket_manager.disconnect(websocket)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "smart-matter-detector",
        "websocket_connections": len(websocket_manager.active_connections)
    }


@app.get("/")
async def root():
    return {
        "message": "Smart Matter Opportunity Detector API",
        "version": "1.0.0"
    }
