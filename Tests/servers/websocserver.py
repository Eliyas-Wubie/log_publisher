import asyncio
import websockets

# Handler for each WebSocket connection
async def echo(websocket):
    async for message in websocket:
        print(f"Received: {message}")
        await websocket.send(f"Echo: {message}")

# Start the server
async def main():
    async with websockets.serve(echo, "127.0.0.1", 9002):
        print("WebSocket server started on ws://127.0.0.1:9002")
        await asyncio.Future()  # run forever

# Run the server
if __name__ == "__main__":
    asyncio.run(main())
