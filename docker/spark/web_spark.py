import websockets
import json
import asyncio
from pyspark.sql import SparkSession
import pymysql

# Spark 세션 시작
spark = SparkSession.builder \
    .appName("ParkingAreaQuery") \
    .config("spark.jars", "./mysql-connector-j-9.1.0/mysql-connector-j-9.1.0.jar") \
    .master("spark://172.19.0.2:7077").getOrCreate()

# MariaDB에서 500m 내의 주차장을 조회하는 함수
def get_parking_nearby(lat, lon):
    # MariaDB에 연결
    connection = pymysql.connect(host="db-server-ip", user="root", password="yourpassword", db="parkingissue", charset='utf8', port=6033)
    cursor = connection.cursor()

    # 500m 내 주차장 조회를 위한 위경도 범위 계산
    ro = 0.0045
    ra = 0.0057
    lo_m = lon - ro
    lo_p = lon + ro
    la_m = lat - ra
    la_p = lat + ra

    # SQL 쿼리 작성
    sql = f"""SELECT park_id, park_nm, park_addr, park_lo, park_la
              FROM parkingarea_info
              WHERE park_lo BETWEEN {lo_m} AND {lo_p}
              AND park_la BETWEEN {la_m} AND {la_p}"""
    
    cursor.execute(sql)
    data = cursor.fetchall()
    connection.close()

    return data

# WebSocket 서버 코드
async def spark_server(websocket, path):
    try:
        # 클라이언트로부터 메시지 받기
        data = await websocket.recv()
        coords = json.loads(data)
        lat = coords.get("lat")
        lon = coords.get("lon")

        # 처리된 결과를 클라이언트로 전송
        response = {"message": f"Received latitude: {lat}, longitude: {lon}"}
        await websocket.send(json.dumps(response))

    except Exception as e:
        print(f"Error: {e}")

# WebSocket 서버 실행
async def main():
    server = await websockets.serve(spark_server, "0.0.0.0", 6789)  # Spark 서버의 IP와 포트
    print("Spark WebSocket Server is running on ws://0.0.0.0:6789")
    await server.wait_closed()

# 비동기 서버 실행
if __name__ == "__main__":
    asyncio.run(main())
