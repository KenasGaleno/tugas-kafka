# Warehouse Monitoring System

Sistem Pemantauan Kondisi Gudang ini menggunakan **Apache Kafka** dan **PySpark** untuk memantau suhu dan kelembaban di gudang penyimpanan barang sensitif, seperti makanan, obat-obatan, dan elektronik. Sistem ini mendeteksi peringatan suhu tinggi dan kelembaban berlebih secara real-time untuk mencegah kerusakan barang.

## Fitur Utama

- **Pemantauan Real-Time**: Data suhu dan kelembaban dikirim setiap detik dan diproses langsung oleh sistem.
- **Peringatan Kondisi Kritis**: Peringatan akan diberikan jika suhu melebihi 80°C atau kelembaban lebih dari 70%.
- **Penggabungan Data**: Data suhu dan kelembaban digabungkan untuk analisis yang lebih komprehensif dan mendeteksi kondisi kritis di gudang.

## Arsitektur Sistem

1. **Kafka Producer**:
   - **Producer Suhu**: Mengirimkan data suhu setiap detik.
   - **Producer Kelembaban**: Mengirimkan data kelembaban setiap detik.

2. **Kafka Consumer (PySpark)**:
   - Mengonsumsi data suhu dan kelembaban dari Kafka secara real-time.
   - Melakukan **filtering** untuk memberikan peringatan suhu tinggi dan kelembaban tinggi.
   - Menggabungkan data suhu dan kelembaban untuk mendeteksi kondisi kritis pada gudang yang sama.

## Topik Kafka

- **sensor-suhu-gudang**: Topik untuk menerima data suhu.
- **sensor-kelembaban-gudang**: Topik untuk menerima data kelembaban.

## Menjalankan Sistem

### 1. Menjalankan Kafka dan Zookeeper

Pastikan Kafka dan Zookeeper sudah berjalan. Anda bisa menggunakan **Docker** untuk menjalankannya dengan mudah:

```bash
docker-compose -f docker-compose.yml up
```

### Menjalankan Kafka Producer dan Dokumentasi

a. Producer Suhu:
Untuk menjalankan producer suhu, gunakan perintah berikut:

```bash
python producer_suhu_sesuai.py
```

![WhatsApp Image 2025-05-23 at 06 05 58_cf690eda](https://github.com/user-attachments/assets/6a0d9122-9171-4dc9-b405-0fc78cff306a)

b. Producer Kelembaban:
Untuk menjalankan producer kelembaban, gunakan perintah berikut:

```bash
python producer_kelembaban_sesuai.py
```

![WhatsApp Image 2025-05-23 at 06 06 23_bbc2b630](https://github.com/user-attachments/assets/2e2fb630-f12c-4399-948c-a831790c66e6)

c. Menjalankan Kafka Consumer dengan PySpark
Setelah Kafka producer mengirimkan data, jalankan consumer PySpark untuk mengonsumsi dan memproses data:

```bash
python pyspark_consumer_sesuai.py
```

![WhatsApp Image 2025-05-23 at 05 55 34_6861df7c](https://github.com/user-attachments/assets/c7347acc-defd-4f96-82ff-082a00134ed0)



