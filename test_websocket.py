#!/usr/bin/env python3
"""WebSocket test client"""

import asyncio
import websockets
import sys


async def test_websocket():
    """Test WebSocket connection"""
    uri = "ws://localhost:8000/ws"

    try:
        print(f"Connecting to {uri}...")
        async with websockets.connect(uri) as websocket:
            print("✓ Connected successfully!")
            print("Listening for notifications (press Ctrl+C to exit)...")

            # Send ping
            await websocket.send("ping")
            print("→ Sent ping")

            # Wait for pong
            response = await websocket.recv()
            print(f"← Received: {response}")

            # Keep listening for binary messages (notifications)
            async for message in websocket:
                if isinstance(message, bytes):
                    print(f"\n📢 Received binary notification ({len(message)} bytes)")
                    print(f"   Raw bytes (first 50): {message[:50]}...")
                else:
                    print(f"← Text message: {message}")

    except websockets.exceptions.ConnectionClosed:
        print("Connection closed")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(test_websocket())
    except KeyboardInterrupt:
        print("\nDisconnected")
