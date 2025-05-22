from pyspark.sql import SparkSession

if __name__ == "__main__":
    try:
        print("Mencoba memulai SparkSession...")
        spark = SparkSession.builder \
            .appName("TestSparkApp") \
            .getOrCreate()

        print("SparkSession berhasil dibuat!")
        print(f"Versi Spark: {spark.version}")

        data = [("Alice", 1), ("Bob", 2)]
        columns = ["nama", "id"]
        df = spark.createDataFrame(data, columns)

        print("DataFrame berhasil dibuat. Menampilkan isi DataFrame:")
        df.show()

        spark.stop()
        print("SparkSession berhasil dihentikan.")

    except Exception as e:
        print("Terjadi error saat menjalankan Spark:")
        import traceback
        traceback.print_exc()