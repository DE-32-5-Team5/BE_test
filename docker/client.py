import websockets
import json

async def send_location():
    uri = "ws://localhost:8000/ws"  # FastAPI WebSocket 서버 주소
    async with websockets.connect(uri) as websocket:
        # 위경도 데이터 보내기
        data = json.dumps({"lat": 37.49655145, "lon": 127.0247831027794})
        await websocket.send(data)

        # FastAPI 서버로부터 결과 받기
        response = await websocket.recv()
        print("Received from FastAPI:", response)

# 비동기 함수 실행
import asyncio
asyncio.run(send_location())

