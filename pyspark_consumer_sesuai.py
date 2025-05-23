from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, avg, round as spark_round, coalesce, current_timestamp, expr, when, lit # Pastikan 'lit' ada di sini
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType
import datetime # Diimpor untuk digunakan di output_batch_to_console

# Konfigurasi Kafka (diubah sesuai producer modifikasi)
KAFKA_BOOTSTRAP_SERVERS_SPARK = 'localhost:29092'
SUHU_TOPIC_SPARK = "monitor-suhu-warehouse"
KELEMBABAN_TOPIC_SPARK = "monitor-kelembaban-warehouse"

# Skema untuk data suhu (disesuaikan dengan producer modifikasi)
schema_suhu_mod = StructType([
    StructField("id_lokasi", StringType(), True),
    StructField("suhu_val", DoubleType(), True),
    StructField("timestamp_event", StringType(), True) # Awalnya string, akan di-cast
])

# Skema untuk data kelembaban (disesuaikan dengan producer modifikasi)
schema_kelembaban_mod = StructType([
    StructField("id_lokasi", StringType(), True),
    StructField("kelembaban_val", DoubleType(), True),
    StructField("timestamp_event", StringType(), True) # Awalnya string, akan di-cast
])

# Batas ideal (contoh)
SUHU_IDEAL_MIN = 18.0
SUHU_IDEAL_MAX = 25.0
KELEMBABAN_IDEAL_MIN = 50.0
KELEMBABAN_IDEAL_MAX = 65.0

# Batas Kritis (lebih lebar dari ideal)
SUHU_KRITIS_ATAS = 30.0
SUHU_KRITIS_BAWAH = 15.0
KELEMBABAN_KRITIS_ATAS = 75.0
KELEMBABAN_KRITIS_BAWAH = 40.0


if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("WarehouseMonitorMod") \
        .master("local[2]") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
        .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true") \
        .config("spark.sql.session.timeZone", "UTC") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    # --- Membaca Stream Suhu ---
    df_suhu_raw = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS_SPARK) \
        .option("subscribe", SUHU_TOPIC_SPARK) \
        .option("startingOffsets", "latest") \
        .load()

    df_suhu_parsed = df_suhu_raw.selectExpr("CAST(value AS STRING) as json_string") \
        .select(from_json(col("json_string"), schema_suhu_mod).alias("data")) \
        .select("data.*") \
        .withColumn("event_ts_suhu", col("timestamp_event").cast(TimestampType())) \
        .withColumnRenamed("id_lokasi", "id_lokasi_s") \
        .withColumnRenamed("suhu_val", "suhu_rata2")

    # Watermark dan Windowing untuk Suhu
    df_suhu_windowed = df_suhu_parsed \
        .withWatermark("event_ts_suhu", "20 seconds") \
        .groupBy(
            window(col("event_ts_suhu"), "15 seconds", "5 seconds").alias("time_window_suhu"), # Alias untuk kolom window
            col("id_lokasi_s")
        ).agg(
            spark_round(avg("suhu_rata2"), 2).alias("suhu_avg")
        )
        # Tidak ada .select(...) di sini agar kolom time_window_suhu tetap ada untuk join

    # --- Membaca Stream Kelembaban ---
    df_kelembaban_raw = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS_SPARK) \
        .option("subscribe", KELEMBABAN_TOPIC_SPARK) \
        .option("startingOffsets", "latest") \
        .load()

    df_kelembaban_parsed = df_kelembaban_raw.selectExpr("CAST(value AS STRING) as json_string") \
        .select(from_json(col("json_string"), schema_kelembaban_mod).alias("data")) \
        .select("data.*") \
        .withColumn("event_ts_kelembaban", col("timestamp_event").cast(TimestampType())) \
        .withColumnRenamed("id_lokasi", "id_lokasi_k") \
        .withColumnRenamed("kelembaban_val", "kelembaban_rata2")

    # Watermark dan Windowing untuk Kelembaban
    df_kelembaban_windowed = df_kelembaban_parsed \
        .withWatermark("event_ts_kelembaban", "20 seconds") \
        .groupBy(
            window(col("event_ts_kelembaban"), "15 seconds", "5 seconds").alias("time_window_kelembaban"), # Alias
            col("id_lokasi_k")
        ).agg(
            spark_round(avg("kelembaban_rata2"), 2).alias("kelembaban_avg")
        )
        # Tidak ada .select(...) di sini agar kolom time_window_kelembaban tetap ada untuk join
        
    # --- Menggabungkan Stream Windowed ---
    # MODIFIKASI DI SINI: Join langsung pada struct window
    joined_df = df_suhu_windowed.join(
        df_kelembaban_windowed,
        expr("""
            id_lokasi_s = id_lokasi_k AND
            time_window_suhu = time_window_kelembaban 
        """), # Join pada kesetaraan struct window
        "full_outer"
    ).select(
        coalesce(col("id_lokasi_s"), col("id_lokasi_k")).alias("id_lokasi"),
        # Ekstrak start dan end dari window yang di-coalesce
        coalesce(col("time_window_suhu.start"), col("time_window_kelembaban.start")).alias("window_start"),
        coalesce(col("time_window_suhu.end"), col("time_window_kelembaban.end")).alias("window_end"),
        col("suhu_avg"),
        col("kelembaban_avg")
    )

    # --- Menentukan Status Gudang ---
    DEFAULT_SUHU_FOR_STATUS = (SUHU_IDEAL_MIN + SUHU_IDEAL_MAX) / 2
    DEFAULT_KELEMBABAN_FOR_STATUS = (KELEMBABAN_IDEAL_MIN + KELEMBABAN_IDEAL_MAX) / 2
    
    status_df = joined_df.withColumn(
        "suhu_cek", coalesce(col("suhu_avg"), lit(DEFAULT_SUHU_FOR_STATUS))
    ).withColumn(
        "kelembaban_cek", coalesce(col("kelembaban_avg"), lit(DEFAULT_KELEMBABAN_FOR_STATUS))
    ).withColumn("status_gudang",
        when((col("suhu_avg").isNull()) & (col("kelembaban_avg").isNull()), "Data Tidak Tersedia")
        .when(col("suhu_avg").isNull(), "Data Suhu Hilang")
        .when(col("kelembaban_avg").isNull(), "Data Kelembaban Hilang")
        .when((col("suhu_cek") > SUHU_KRITIS_ATAS) & (col("kelembaban_cek") > KELEMBABAN_KRITIS_ATAS), "KRITIS: Panas & Lembab Berlebih!")
        .when((col("suhu_cek") < SUHU_KRITIS_BAWAH) & (col("kelembaban_cek") < KELEMBABAN_KRITIS_BAWAH), "KRITIS: Dingin & Kering Berlebih!")
        .when(col("suhu_cek") > SUHU_KRITIS_ATAS, "PERINGATAN: Suhu Terlalu Panas!")
        .when(col("suhu_cek") < SUHU_KRITIS_BAWAH, "PERINGATAN: Suhu Terlalu Dingin!")
        .when(col("kelembaban_cek") > KELEMBABAN_KRITIS_ATAS, "PERINGATAN: Kelembaban Terlalu Tinggi!")
        .when(col("kelembaban_cek") < KELEMBABAN_KRITIS_BAWAH, "PERINGATAN: Kelembaban Terlalu Rendah!")
        .when(
            (col("suhu_cek").between(SUHU_IDEAL_MIN, SUHU_IDEAL_MAX)) &
            (col("kelembaban_cek").between(KELEMBABAN_IDEAL_MIN, KELEMBABAN_IDEAL_MAX)),
            "Kondisi Optimal"
        )
        .otherwise("Kondisi Perlu Perhatian")
    )

    # --- Output ke Konsol ---
    def output_batch_to_console(batch_df, epoch_id):
        print(f"\n--- Laporan Status Gudang (Batch: {epoch_id}, Waktu Proses: {datetime.datetime.now()}) ---") # Menggunakan datetime
        if batch_df.count() > 0:
            batch_df.select(
                "id_lokasi",
                "window_start",
                "window_end",
                spark_round("suhu_avg",1).alias("Suhu (°C)"),
                spark_round("kelembaban_avg",1).alias("Kelembaban (%)"),
                "status_gudang"
            ).orderBy("id_lokasi", "window_start").show(truncate=False)
        else:
            print("Tidak ada data baru di batch ini.")
        print("--- Akhir Laporan Batch ---\n")

    query_console = status_df.writeStream \
        .outputMode("append") \
        .trigger(processingTime="10 seconds") \
        .foreachBatch(output_batch_to_console) \
        .start()

    query_console.awaitTermination()
