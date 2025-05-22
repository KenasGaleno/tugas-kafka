import json
import time
import random
from kafka import KafkaProducer
import datetime

KAFKA_TOPIC_NAME_MOD = "monitor-suhu-warehouse" # Nama topik diubah
KAFKA_BOOTSTRAP_SERVERS_MOD = 'localhost:29092'

WAREHOUSE_IDS_MOD = ["WH-A", "WH-B", "WH-C", "WH-D"] # ID Gudang diubah dan ditambah

if __name__ == "__main__":
    print("Memulai Kafka Producer Suhu...")
    producer_suhu = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS_MOD,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    try:
        while True:
            warehouse_id = random.choice(WAREHOUSE_IDS_MOD)
            # Simulasikan suhu (misal antara 18 dan 35 Celcius)
            suhu_celsius = random.uniform(18.0, 28.0) # Menggunakan float untuk suhu
            if random.random() < 0.08:  # 8% chance of spike
                if random.random() < 0.5:
                     suhu_celsius = random.uniform(28.1, 35.0) # Spike panas
                else:
                     suhu_celsius = random.uniform(10.0, 17.9) # Spike dingin

            message_suhu = {
                "id_lokasi": warehouse_id,
                "suhu_val": round(suhu_celsius, 2), # Nama field diubah, dibulatkan
                "timestamp_event": datetime.datetime.now().isoformat() # Format timestamp diubah
            }
            print(f"Mengirim data suhu (mod): {message_suhu}")
            producer_suhu.send(KAFKA_TOPIC_NAME_MOD, message_suhu)
            producer_suhu.flush()
            time.sleep(random.uniform(0.8, 1.2)) # Interval pengiriman sedikit divariasikan
    except KeyboardInterrupt:
        print("Producer Suhu (mod) dihentikan.")
    finally:
        producer_suhu.close()
        print("Koneksi Producer Suhu (mod) ditutup.")