# tugas-kafka

# Warehouse Monitoring System

Sistem Pemantauan Kondisi Gudang menggunakan **Apache Kafka** dan **PySpark** untuk memantau suhu dan kelembaban secara real-time. Sistem ini dirancang untuk membantu perusahaan logistik yang mengelola gudang penyimpanan barang sensitif seperti makanan, obat-obatan, dan elektronik, dengan tujuan untuk mencegah kerusakan barang akibat suhu terlalu tinggi atau kelembaban berlebih.

## Fitur Utama

- **Pemantauan Real-Time**: Data suhu dan kelembaban dikirim setiap detik dan diproses langsung oleh sistem.
- **Peringatan Kondisi Kritis**: Sistem memberikan peringatan jika suhu lebih dari 80°C atau kelembaban lebih dari 70%, serta menggabungkan kedua kondisi untuk mendeteksi peringatan kritis.
- **Penggabungan Data**: Data suhu dan kelembaban digabungkan berdasarkan waktu dan ID gudang untuk analisis yang lebih komprehensif.

## Arsitektur Sistem

1. **Kafka Producer**:
   - **Producer Suhu**: Mengirimkan data suhu setiap detik.
   - **Producer Kelembaban**: Mengirimkan data kelembaban setiap detik.

2. **Kafka Consumer (PySpark)**:
   - Mengonsumsi data suhu dan kelembaban dari Kafka secara real-time.
   - Melakukan filtering untuk memberikan peringatan suhu tinggi dan kelembaban tinggi.
   - Menggabungkan data suhu dan kelembaban untuk mendeteksi kondisi kritis pada gudang yang sama.

## Topik Kafka

- **sensor-suhu-gudang**: Topik untuk menerima data suhu.
- **sensor-kelembaban-gudang**: Topik untuk menerima data kelembaban.

## Menjalankan Sistem

### 1. Menjalankan Kafka dan Zookeeper

Pastikan Kafka dan Zookeeper sudah berjalan. Anda bisa menggunakan **Docker** untuk menjalankannya dengan mudah.

```bash
docker-compose -f docker-compose.yml up
Menjalankan Kafka Producer
a. Producer Suhu:
Untuk menjalankan producer suhu, gunakan perintah berikut:

bash
Salin
Edit
python producer_suhu_sesuai.py
b. Producer Kelembaban:
Untuk menjalankan producer kelembaban, gunakan perintah berikut:

bash
Salin
Edit
python producer_kelembaban_sesuai.py
3. Menjalankan Kafka Consumer dengan PySpark
Setelah Kafka producer mengirimkan data, jalankan consumer PySpark untuk mengonsumsi dan memproses data:

bash
Salin
Edit
python pyspark_consumer_sesuai.py
4. Memeriksa Output
Setelah menjalankan producer dan consumer, Anda akan melihat output di konsol yang menunjukkan status setiap gudang. Output ini mencakup suhu, kelembaban, dan status kondisi gudang (seperti "Kondisi Optimal", "PERINGATAN: Suhu Terlalu Panas!", atau "PERINGATAN KRITIS").

5. Menghentikan Proses
Untuk menghentikan producer atau consumer, tekan Ctrl+C di terminal tempat Anda menjalankan skrip.

Struktur Direktori
bash
Salin
Edit
├── producer_suhu_sesuai.py    # Kafka Producer untuk suhu
├── producer_kelembaban_sesuai.py  # Kafka Producer untuk kelembaban
├── pyspark_consumer_sesuai.py  # Kafka Consumer untuk PySpark
├── test_spark.py              # Pengujian SparkSession
├── docker-compose.yml         # Konfigurasi untuk Kafka dan Zookeeper (menggunakan Docker)
├── README.md                  # Dokumentasi proyek ini
Prasyarat
Apache Kafka dan Zookeeper.

Python 3.x dengan pustaka berikut:

kafka-python

pyspark

json

datetime

Instal pustaka yang diperlukan dengan menggunakan pip:

bash
Salin
Edit
pip install kafka-python pyspark
