from pyspark.sql import SparkSession

# Docker 내 Spark Master의 IP 주소 (Spark Master 컨테이너의 IP를 확인)
spark = SparkSession.builder \
    .appName("PySpark Example") \
    .master("spark://172.19.0.2:7077").getOrCreate()

ip = input("input ip adress : ")
port = "3306" 
user = "root"
passwd = input("input db pw code : ")
db = "parkingissue"
table_name = "parkingarea_info"

lo = 37.5176288053129
la = 127.086737282438

lo_m = lo - 0.09
lo_p = lo + 0.09

la_m = la - 0.11364
la_p = la + 0.11364

# PySpark 코드 실행
sql = f"""select park_id, park_nm, park_addr, park_lo, park_la 
from parkingarea_info
where park_lo between {lo_m} and {lo_p} and park_la between {la_m} and {la_p};
"""
df = spark.read.format("jdbc") \
                .option("url", f"jdbc:mysql://{ip}:{port}/{db}") \
                .option("driver", "com.mysql.cj.jdbc.Driver") \
                .option("dbtable", table_name) \
                .option("query", sql) \
                .option("user", user) \
                .option("password", passwd) \
                .load()

df.show()
