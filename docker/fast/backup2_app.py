from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
import websockets
import json

app = FastAPI()

# Spark WebSocket 서버 URI (Spark 서버의 IP 및 포트)
SPARK_WS_URI = "ws://0.0.0.0:6789"  # Spark WebSocket 서버의 주소 (로컬에서 실행 중이면 0.0.0.0 사용)

# WebSocket을 통해 Spark에 데이터 전송 및 결과 받기
async def send_to_spark(lat, lon):
    try:
        # Spark WebSocket 서버에 연결
        async with websockets.connect(SPARK_WS_URI) as websocket:
            # 위경도 데이터를 Spark에 전달
            message = json.dumps({"lat": lat, "lon": lon})
            await websocket.send(message)

            # Spark에서 처리된 결과를 받아 반환
            result = await websocket.recv()
            return json.loads(result)
    except Exception as e:
        print(f"Error in send_to_spark: {e}")
        return {"error": "Failed to connect to Spark server or process the request."}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # 클라이언트로부터 위경도 데이터 받기
            data = await websocket.receive_text()
            coords = json.loads(data)
            lat = coords["lat"]
            lon = coords["lon"]

            # Spark 서버에 데이터 전달하여 결과 받기
            result = await send_to_spark(lat, lon)

            # 처리된 결과를 클라이언트로 전송
            await websocket.send_text(json.dumps(result))

    except WebSocketDisconnect:
        print("클라이언트 연결 끊김")

