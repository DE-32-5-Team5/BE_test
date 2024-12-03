from pyspark.sql import SparkSession

# Docker 내 Spark Master의 IP 주소 (Spark Master 컨테이너의 IP를 확인)
spark = SparkSession.builder \
    .appName("PySpark Example") \
    .master("spark://172.19.0.2:7077").getOrCreate()

# PySpark 코드 실행
data = [("James", "Smith", "USA", 30),
        ("Michael", "Rose", "USA", 40),
        ("Robert", "Williams", "USA", 45),
        ("Maria", "Jones", "USA", 35)]
columns = ["first_name", "last_name", "country", "age"]

df = spark.createDataFrame(data, columns)
df.show()
