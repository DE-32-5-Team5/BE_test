from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import pymysql
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

from fastapi.middleware.cors import CORSMiddleware
import json

# MariaDB에서 SELECT SLEEP 쿼리를 수행하는 함수
def get_db(lat: float, lon: float): # lat -> 37.. 인데 DB상으로는 park_lo, lon -> 127.. 인데 DB상으로는 park_la
    # 주변 500m 위경도 계산
    ra = 0.0045 # 위도
    ro = 0.00565 # 경도
    # DB값이 서로 바뀌었기 때문에 계산에서 이름 변경
    lo_m = lon - ro
    lo_p = lon + ro
    la_m = lat - ra
    la_p = lat + ra

    # MariaDB에 연결
    connection = pymysql.connect(host="43.203.116.103", user="root", password="samdul2024$", db="parkingissue", charset='utf8', port = 6033)
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    # DB에 park_la에 경도가 있고 park_lo에 위도가 있음 서로 바뀌어 버린 상황
    sql = f"""
    SELECT park_id, park_nm, park_addr, park_lo, park_la,
        (6371 * acos(cos(radians({lat})) * cos(radians(park_lo)) * cos(radians(park_la) - radians({lon})) + sin(radians({lat})) * sin(radians(park_lo)))) AS distance
    FROM parkingarea_info
    WHERE park_la BETWEEN {la_m} AND {la_p}
          AND park_lo BETWEEN {lo_m} AND {lo_p}
    ORDER BY distance ASC
    limit 20
    """

    cursor.execute(sql)
    data = cursor.fetchall()
    connection.close()

    #json_df = json.dumps(data, ensure_ascii=False, indent = 4)

    return data

app = FastAPI()

# CORS 설정 추가 
origins = [
        "http://localhost:5500",
        "http://localhost:8000", 
        "http://127.0.0.1:8000"
        ] 
app.add_middleware( 
        CORSMiddleware, 
        allow_origins=origins, 
        allow_credentials=True, 
        allow_methods=["*"], 
        allow_headers=["*"], 
        )

@app.get("/items/")
def read_items():
    #db = next(get_db())
    st = time.time()
    df = get_db(37.2635846787744, 127.028715898311)
    end = time.time()
    all_time = end - st
    # ... 데이터베이스 쿼리 실행 ...
    return df

@app.get("/location")
async def receive_location(latitude: float, longitude: float):
    dic = get_db(latitude, longitude)
    print(dic)
    return dic
