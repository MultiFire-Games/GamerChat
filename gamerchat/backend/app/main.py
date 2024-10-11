from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from manager import ConnectionManager

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = ConnectionManager()

@app.websocket("/rtc")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Accept WebSocket connection
    data = await websocket.receive_json()
    if data['type'] == 'join':
        nick = data['nick']
        await manager.connect(websocket, nick)
    try:
        while True:
            data = await websocket.receive_json()
            if data['type'] == 'chat_message':
                await manager.broadcast_message(data['nick'], data['content'])
            # Add more RTC-related handling here
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast_user_list()
