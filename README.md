# Evaluasi Kinerja Database SQL, NoSQL, dan In-Memory pada Sistem E-Commerce
### Studi Kasus: Optimasi Katalog Produk dan Keranjang Belanja

**Mata Kuliah:** Sistem Basis Data Modern
**Sub-CPMK:** 3.4 — Evaluasi kinerja sistem basis data dalam solusi industri
**Kelompok:** 6

---

## 1. Deskripsi Proyek

Proyek ini mengevaluasi kinerja tiga jenis sistem basis data — **SQL**,
**NoSQL**, dan **In-Memory Database** — dalam konteks solusi industri
e-commerce. Evaluasi difokuskan pada tiga skenario nyata yang masing-masing
cocok dengan karakteristik database yang berbeda:

| Skenario                     | Database              | Alasan Pemilihan                                                 |
|-------------------------------|------------------------|--------------------------------------------------------------------|
| Data transaksi/order          | SQLite (SQL)           | Butuh konsistensi (ACID) dan relasi antar data                    |
| Katalog produk                | TinyDB (NoSQL)         | Skema fleksibel, atribut produk bervariasi antar kategori          |
| Keranjang belanja & session    | fakeredis (In-Memory)  | Butuh akses baca/tulis super cepat, sifat data sementara           |

> **Catatan implementasi:** Proyek ini menggunakan SQLite, TinyDB, dan
> fakeredis sebagai representasi masing-masing jenis database. Ketiganya
> dipilih agar proyek dapat dijalankan murni dengan Python (`pip install`)
> tanpa memerlukan instalasi server database terpisah (PostgreSQL/MongoDB/
> Redis) atau Docker. Karakteristik inti dari tiap jenis database (skema
> ketat vs fleksibel, transaksi ACID, penyimpanan in-memory) tetap
> dipertahankan, sehingga hasil evaluasi kinerja tetap valid secara konsep
> dan dapat digeneralisasi ke database "asli" pada skenario produksi.

## 2. Tujuan Pembelajaran

Sesuai Sub-CPMK-3.4, proyek ini bertujuan untuk mengembangkan kemampuan mahasiswa
dalam mengevaluasi kinerja sistem basis data secara kritis menggunakan metode dan
metrik evaluasi yang tepat, serta mengidentifikasi dan memecahkan masalah kinerja
yang muncul dalam skenario industri nyata.

## 3. Metrik yang Diukur

- **Write Latency & Throughput** — kecepatan dan jumlah operasi tulis (insert) per detik
- **Read Latency & Throughput** — kecepatan dan jumlah operasi baca (query) per detik
- Pengujian dilakukan pada 3 volume data berbeda: **100, 1.000, dan 5.000 record**
  untuk melihat bagaimana kinerja masing-masing database berubah seiring
  bertambahnya skala data.

## 4. Struktur Folder

```
TUGAS KELOMPOK 6 SISTEM BASIS DATA/
├── requirements.txt             # Dependency Python
├── README.md                    # Dokumentasi proyek (file ini)
├── scripts/
│   ├── generate_data.py         # Generator data dummy e-commerce
│   ├── benchmark_sql.py         # Benchmark SQLite (data order)
│   ├── benchmark_nosql.py       # Benchmark TinyDB (data produk)
│   ├── benchmark_inmemory.py    # Benchmark fakeredis (data cart)
│   └── run_all_benchmarks.py    # Script utama: jalankan semua & generate laporan
├── data/                        # File database lokal (dihasilkan otomatis)
│   ├── orders.db                # SQLite
│   └── products.json            # TinyDB
└── results/
    ├── comparison_results.csv   # Hasil benchmark (dihasilkan otomatis)
    └── throughput_comparison.png# Grafik perbandingan (dihasilkan otomatis)
```

## 5. Cara Menjalankan Proyek

Proyek ini **tidak memerlukan Docker maupun instalasi server database**.
Semua database berjalan murni di dalam Python.

### a. Install dependency Python

Disarankan menggunakan virtual environment:

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### b. Jalankan benchmark

```bash
cd scripts
python run_all_benchmarks.py
```

Script ini akan:
1. Menjalankan benchmark write & read pada PostgreSQL, MongoDB, dan Redis
2. Menampilkan tabel ringkasan hasil di terminal
3. Menyimpan hasil ke `results/comparison_results.csv`
4. Menyimpan grafik perbandingan ke `results/throughput_comparison.png`

## 6. Hasil dan Analisis (Contoh Interpretasi)

Setelah menjalankan benchmark, umumnya pola hasil yang didapat:

- **In-Memory Database (fakeredis)** memiliki throughput write & read tertinggi
  karena beroperasi sepenuhnya di memori (RAM), sangat cocok untuk data sementara
  seperti keranjang belanja.
- **NoSQL (TinyDB)** memiliki kinerja write yang cukup baik untuk data dengan
  skema bervariasi (produk dengan atribut berbeda-beda per kategori) karena
  tidak perlu migrasi skema.
- **SQL (SQLite)** relatif lebih lambat dibanding keduanya untuk operasi masif,
  namun memberikan jaminan konsistensi data (ACID) yang penting untuk transaksi
  keuangan seperti order pembayaran.

> Catatan: pola relatif ini (in-memory > NoSQL > SQL dari sisi kecepatan mentah)
> umumnya konsisten dengan karakteristik database "asli" (Redis, MongoDB,
> PostgreSQL) pada skenario produksi, meskipun angka mutlaknya akan berbeda
> karena skala environment yang berbeda.

**Rekomendasi Arsitektur:** Untuk sistem e-commerce skala menengah-besar,
disarankan menggunakan **arsitektur database hybrid** (dalam implementasi
produksi menggunakan database "asli"):
- PostgreSQL untuk data transaksi/pembayaran
- MongoDB untuk katalog produk
- Redis untuk cache, session, dan keranjang belanja

Pendekatan ini disebut *polyglot persistence*, yaitu menggunakan jenis database
yang berbeda sesuai karakteristik data dan kebutuhan masing-masing modul aplikasi,
alih-alih memaksakan satu jenis database untuk seluruh sistem.

## 7. Anggota Kelompok 6

- Muhammad Iqram Hasan Basri (105841118324)
- Muh. Arya Anggara (105841118624)
- Faidul (105841119824)
- Ryan Prayudha (105841120524)
- Muh. Ikram Maulana (105841120824)
- Salman Alfarisi (105841121224)
