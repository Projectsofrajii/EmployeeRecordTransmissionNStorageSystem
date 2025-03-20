import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://127.0.0.1:8000/ws/employees/"
    
    async with websockets.connect(uri) as websocket:
        # Receive initial connection message
        message = await websocket.recv()
        print(f"Server: {message}")

        # Send test data
        data = {"employee_id": "E123", "name": "John Doe"}
        await websocket.send(json.dumps(data))

        # Receive response
        response = await websocket.recv()
        print(f"Server: {response}")

asyncio.run(test_websocket())
