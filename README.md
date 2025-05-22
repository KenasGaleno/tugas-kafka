# tugas-kafka

Warehouse Monitoring System
Sistem pemantauan kondisi gudang ini dirancang untuk memantau suhu dan kelembaban di beberapa gudang penyimpanan barang sensitif, seperti makanan, obat-obatan, dan elektronik. Sistem ini menggunakan Apache Kafka untuk pengiriman data secara real-time dan PySpark untuk pemrosesan data. Dengan sistem ini, perusahaan dapat mengidentifikasi dan merespons kondisi berbahaya (seperti suhu atau kelembaban yang terlalu tinggi) dengan cepat untuk mencegah kerusakan barang.

Fitur Utama
Pemantauan Real-Time: Data suhu dan kelembaban dikirimkan setiap detik dan diproses secara langsung.

Peringatan Kondisi Kritis: Sistem memberikan peringatan jika suhu lebih dari 80°C atau kelembaban lebih dari 70%, serta menggabungkan kedua kondisi untuk mendeteksi peringatan kritis.

Penggabungan Data: Data suhu dan kelembaban digabungkan berdasarkan waktu dan ID gudang untuk analisis yang lebih komprehensif.

Arsitektur
Kafka Producer:

Producer Suhu: Mengirimkan data suhu setiap detik.

Producer Kelembaban: Mengirimkan data kelembaban setiap detik.

Kafka Consumer:

Mengonsumsi data suhu dan kelembaban dari Kafka menggunakan PySpark.

Melakukan filtering untuk mendeteksi suhu tinggi dan kelembaban tinggi, serta status kondisi gudang yang optimal atau membutuhkan perhatian.

Menggabungkan data suhu dan kelembaban untuk mendeteksi kondisi kritis pada gudang yang sama.

Cara Kerja
1. Kafka Topics
Sistem ini menggunakan dua topik Kafka untuk menerima data sensor secara real-time:

monitor-suhu-warehouse: Untuk data suhu.

monitor-kelembaban-warehouse: Untuk data kelembaban.

2. Simulasi Data Sensor (Producer Kafka)
Dua produser Kafka dikembangkan untuk mensimulasikan pengiriman data suhu dan kelembaban:

Producer Suhu: Mengirimkan data suhu dalam format berikut:

json
Salin
Edit
{"id_lokasi": "G1", "suhu": 82, "timestamp_event": "2025-05-23T05:37:00"}
Producer Kelembaban: Mengirimkan data kelembaban dalam format berikut:

json
Salin
Edit
{"id_lokasi": "G1", "kelembaban": 75, "timestamp_event": "2025-05-23T05:37:00"}
3. Konsumsi dan Olah Data dengan PySpark
PySpark digunakan untuk mengonsumsi dan memproses data dari Kafka:

Filter Data: Sistem ini memfilter suhu yang lebih dari 80°C dan kelembaban yang lebih dari 70% untuk memberikan peringatan.

Gabungkan Stream: Data suhu dan kelembaban digabungkan berdasarkan gudang_id dan window waktu untuk mendeteksi kondisi kritis di gudang yang sama.

4. Peringatan Gabungan
Jika suhu lebih dari 80°C dan kelembaban lebih dari 70% pada gudang yang sama dalam periode waktu yang sama, sistem akan mengeluarkan peringatan kritis:

text
Salin
Edit
[PERINGATAN KRITIS] Gudang G1: - Suhu: 84°C - Kelembaban: 73% - Status: Bahaya tinggi! Barang berisiko rusak
Menjalankan Sistem
1. Menjalankan Kafka dan Zookeeper
Pastikan Kafka dan Zookeeper berjalan. Anda dapat menggunakan Docker untuk menyiapkannya dengan mudah:

bash
Salin
Edit
docker-compose -f docker-compose.yml up
2. Menjalankan Kafka Producer
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
Setelah produser mengirimkan data ke Kafka, jalankan consumer PySpark untuk mengonsumsi dan memproses data:

bash
Salin
Edit
python pyspark_consumer_sesuai.py
4. Memeriksa Output
Setelah menjalankan produser dan consumer, Anda akan melihat output di konsol yang menunjukkan status setiap gudang. Output ini mencakup suhu, kelembaban, dan status kondisi gudang (seperti "Kondisi Optimal", "PERINGATAN: Suhu Terlalu Panas!", atau "PERINGATAN KRITIS").

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
