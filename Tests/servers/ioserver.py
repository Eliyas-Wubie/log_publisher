import socketio
from aiohttp import web

# Create a Socket.IO server
sio = socketio.AsyncServer(cors_allowed_origins='*')
app = web.Application()
sio.attach(app)

# Event handler for new connections
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit('message', 'Welcome!', to=sid)

# Event handler for messages
@sio.event
async def message(sid, data):
    print(f"Received message from {sid}: {data}")
    await sio.emit('message', f"Echo: {data}")

# Event handler for disconnection
@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

# Start server
if __name__ == '__main__':
    web.run_app(app,host="127.0.0.1", port=9001)
