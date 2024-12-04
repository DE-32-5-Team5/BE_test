from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import pymysql
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

lo = 37.2484198802837
la = 127.058484853485

ro = 0.0045
ra = 0.0057

lo_m = lo - ro
lo_p = lo + ro
la_m = la - ra
la_p = la + ra

# MariaDB에서 SELECT SLEEP 쿼리를 수행하는 함수
def get_db():
    # MariaDB에 연결
    connection = pymysql.connect(host="43.203.132.45", user="root", password="samdul2024$", db="parkingissue", charset='utf8', port = 6033)
    cursor = connection.cursor()
    sql = f"""select park_id, park_nm, park_addr, park_lo, park_la
    from parkingarea_info
    where park_lo between {lo_m} and {lo_p}
    and park_la between {la_m} and {la_p}
    """
    cursor.execute(sql)
    data = cursor.fetchall()
    connection.close()

    return data

app = FastAPI()
@app.get("/items/")
def read_items():
    #db = next(get_db())
    st = time.time()
    df = get_db()
    end = time.time()
    all_time = end - st
    # ... 데이터베이스 쿼리 실행 ...
    return df, all_time

# 클라이언트로부터 받은 메시지를 외부 WebSocket 서버로 전달
async def send_to_websocket_server(uri: str, message: str):
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        response = await websocket.recv()
        print(f"서버 응답: {response}")
        return response

# WebSocket 엔드포인트
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # 클라이언트로부터 메시지 수신
            data = await websocket.receive_text()
            print(f"클라이언트로부터 받은 메시지: {data}")

            # 데이터베이스에서 직접 조회 명령
            if data == "get_parking":
                db_data = get_db()
                await websocket.send_text(f"Parking Data: {db_data}")
            else:
                # 외부 WebSocket 서버로 메시지 전달
                uri = "spark://172.19.0.2:7077"  # 외부 WebSocket 서버 URI
                response = await send_to_websocket_server(uri, data)

                # 외부 서버의 응답을 클라이언트로 전달
                await websocket.send_text(f"외부 서버 응답: {response}")
    except WebSocketDisconnect:
        print("클라이언트 연결 끊김")

# HTML 테스트 페이지
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>WebSocket Test</title>
    </head>
    <body>
        <h1>WebSocket Test</h1>
        <button onclick="sendMessage()">Get Parking Data</button>
        <button onclick="sendCustomMessage()">Send Custom Message</button>
        <ul id="messages"></ul>
        <script>
            const ws = new WebSocket("ws://localhost:8000/ws");

            ws.onmessage = (event) => {
                const messages = document.getElementById("messages");
                const message = document.createElement("li");
                message.textContent = event.data;
                messages.appendChild(message);
            };

            function sendMessage() {
                ws.send("get_parking");
            }

            function sendCustomMessage() {
                const customMessage = prompt("Enter your message:");
                if (customMessage) {
                    ws.send(customMessage);
                }
            }
        </script>
    </body>
</html>
"""

@app.get("/")
def get():
    return HTMLResponse(html)
