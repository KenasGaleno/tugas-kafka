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

### dewfvw
