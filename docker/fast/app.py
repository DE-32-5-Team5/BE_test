from fastapi import FastAPI, HTTPException, WebSocket
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
