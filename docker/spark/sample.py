from pyspark.sql import SparkSession
# import pandas as pd

# Docker 내 Spark Master의 IP 주소 (Spark Master 컨테이너의 IP를 확인)
spark = SparkSession.builder \
    .appName("PySpark Example") \
    .config("spark.jars",
        "./mysql-connector-j-9.1.0/mysql-connector-j-9.1.0.jar") \
    .master("spark://172.19.0.2:7077").getOrCreate()

db_ip = input("input db_ip adress : ")
kafka_ip = input("input kafka_ip adress : ")
port = "6033" 
user = "fiveguys"
passwd = input("input db pw code : ")
db = "parkingissue"
table_name = "parkingarea_info"

lo = 37.49655145
la = 127.0247831027794

ro = 0.0045
ra = 0.0057

lo_m = lo - ro
lo_p = lo + ro
la_m = la - ra
la_p = la + ra

def kafka():
    # Kafka 스트리밍 데이터 읽기
    kafka_df = spark.readStream.format("kafka") \
        .option("kafka.bootstrap.servers", f"{kafka_ip}:9092") \
        .option("subscribe", "location_topic") \
        .load()
    return kafka_df

def jdbc():
    df = spark.read.format("jdbc") \
                .option("url", f"jdbc:mysql://{ip}:{port}/{db}") \
                .option("driver", "com.mysql.cj.jdbc.Driver") \
                .option("query", sql) \
                .option("user", user) \
                .option("password", passwd) \
                .load()
    return df

# 주변 500m 이내 주차장 정보 조회
def parkslot():
    sql = f"""select park_id, park_nm, park_addr, park_lo, park_la 
    from parkingarea_info
    where park_lo between {lo_m} and {lo_p}
    and park_la between {la_m} and {la_p}
    """
    df = jdbc()
    parkslotJson = df.toJSON().collect()
    return parkslotJson # 여기에서 json 으로 값 반환
