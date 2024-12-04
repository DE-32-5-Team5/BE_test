from pyspark.sql import SparkSession

# Docker 내 Spark Master의 IP 주소 (Spark Master 컨테이너의 IP를 확인)
spark = SparkSession.builder \
        .config("spark.jars",
                "./mysql-connector-j-9.1.0/mysql-connector-j-9.1.0.jar") \
        .appName("PySpark Example") \
        .master("spark://172.19.0.2:7077").getOrCreate()

ip = input("input ip adress : ")
port = "6033" 
user = "root"
passwd = input("input db pw code : ")
db = "parkingissue"
table_name = "parkingarea_info"

lo = 37.5176288053129
la = 127.086737282438

lo_m = lo - 0.009
lo_p = lo + 0.009

la_m = la - 0.0103
la_p = la + 0.0103

# PySpark 코드 실행
sql = f"""
SELECT park_id, park_nm, park_addr, park_lo, park_la 
FROM parkingarea_info
WHERE park_lo BETWEEN {lo_m} AND {lo_p}
AND park_la BETWEEN {la_m} AND {la_p}
"""

df = spark.read.format("jdbc") \
                .option("url", f"jdbc:mysql://{ip}:{port}/{db}") \
                .option("driver", "com.mysql.cj.jdbc.Driver") \
                .option("query", sql) \
                .option("user", user) \
                .option("password", passwd) \
                .load()

result = df.toJSON().collect()
print(result)

