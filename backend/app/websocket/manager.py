"""WebSocket connection manager for broadcasting notifications"""

from fastapi import WebSocket, WebSocketDisconnect
from typing import Set
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections for real-time notifications"""

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        """
        Accept and register new WebSocket connection.

        Args:
            websocket: WebSocket connection to accept
        """
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """
        Remove WebSocket connection.

        Args:
            websocket: WebSocket connection to remove
        """
        self.active_connections.discard(websocket)
        logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, message: bytes):
        """
        Broadcast protobuf message to all connected clients.

        Args:
            message: Serialized protobuf message bytes
        """
        disconnected = set()

        for connection in self.active_connections.copy():
            try:
                await connection.send_bytes(message)
                logger.debug(f"Sent notification to client")
            except WebSocketDisconnect:
                disconnected.add(connection)
                logger.warning("Client disconnected during broadcast")
            except Exception as e:
                logger.error(f"Error sending to client: {e}")
                disconnected.add(connection)

        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)

    async def send_to_client(self, websocket: WebSocket, message: bytes):
        """
        Send message to specific client.

        Args:
            websocket: WebSocket connection to send to
            message: Serialized protobuf message bytes
        """
        try:
            await websocket.send_bytes(message)
        except Exception as e:
            logger.error(f"Error sending to specific client: {e}")
            self.disconnect(websocket)


# Global connection manager instance
manager = ConnectionManager()
