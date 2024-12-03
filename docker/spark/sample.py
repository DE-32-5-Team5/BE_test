from pyspark.sql import SparkSession

# Docker 내 Spark Master의 IP 주소 (Spark Master 컨테이너의 IP를 확인)
spark = SparkSession.builder \
    .appName("PySpark Example") \
    .master("spark://172.20.0.2:7077").getOrCreate()

ip = input("input ip adress : ")
port = "3306" 
user = "fiveguys"
passwd = input("input db pw code : ")
db = "parkingissue"
table_name = "parkingarea_info"

lo = 37.49655145
la = 127.0247831027794

# PySpark 코드 실행
sql = f"""select park_id, park_nm, park_addr 
from parkingarea_info
where park_lo between {lo} - 0.0045 and {lo} + 0.0045
and park_la between {la} - 0.0057 and {la} + 0.0057
limit 5;
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
