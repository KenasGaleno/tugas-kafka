import json
import time
import random
from kafka import KafkaProducer
import datetime

KAFKA_TOPIC_NAME_MOD = "monitor-kelembaban-warehouse" # Nama topik diubah
KAFKA_BOOTSTRAP_SERVERS_MOD = 'localhost:29092'

WAREHOUSE_IDS_MOD = ["WH-A", "WH-B", "WH-C", "WH-D"] # ID Gudang disamakan dengan producer suhu

if __name__ == "__main__":
    print("Memulai Kafka Producer Kelembaban...")
    producer_kelembaban = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS_MOD,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    try:
        while True:
            warehouse_id = random.choice(WAREHOUSE_IDS_MOD)
            # Simulasikan kelembaban (misal antara 40% dan 85%)
            kelembaban_persen = random.uniform(45.0, 70.0) # Menggunakan float
            if random.random() < 0.07:  # 7% chance of spike
                if random.random() < 0.5:
                    kelembaban_persen = random.uniform(70.1, 85.0) # Spike tinggi
                else:
                    kelembaban_persen = random.uniform(30.0, 44.9) # Spike rendah


            message_kelembaban = {
                "id_lokasi": warehouse_id,
                "kelembaban_val": round(kelembaban_persen, 2), # Nama field diubah, dibulatkan
                "timestamp_event": datetime.datetime.now().isoformat() # Format timestamp diubah
            }
            print(f"Mengirim data kelembaban (mod): {message_kelembaban}")
            producer_kelembaban.send(KAFKA_TOPIC_NAME_MOD, message_kelembaban)
            producer_kelembaban.flush()
            time.sleep(random.uniform(0.9, 1.1)) # Interval pengiriman sedikit divariasikan
    except KeyboardInterrupt:
        print("Producer Kelembaban (mod) dihentikan.")
    finally:
        producer_kelembaban.close()
        print("Koneksi Producer Kelembaban (mod) ditutup.")