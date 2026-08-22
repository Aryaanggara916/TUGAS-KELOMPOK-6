"""
benchmark_nosql.py
---------------------
Mengukur kinerja database NoSQL/dokumen untuk skenario katalog produk
pada sistem e-commerce, menggunakan TinyDB.

Catatan: TinyDB dipilih sebagai representasi database NoSQL karena
tidak memerlukan instalasi server terpisah (murni Python + file JSON),
namun tetap merepresentasikan karakteristik inti NoSQL dokumen: skema
fleksibel (setiap dokumen bisa punya struktur berbeda) dan query
berbasis dokumen -- sehingga hasil analisis kinerja tetap valid untuk
dibandingkan dengan SQL dan In-Memory Database.

Metrik yang diukur:
- Write latency & throughput (insert dokumen)
- Read latency & throughput (query berdasarkan kategori)
"""

import os
import time
from tinydb import TinyDB, Query
from generate_data import generate_products

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "products.json")


def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    return TinyDB(DB_PATH)


def benchmark_write(db, products):
    start = time.perf_counter()
    db.insert_multiple(products)
    elapsed = time.perf_counter() - start
    return elapsed


def benchmark_read(db, sample_size=100):
    Product = Query()
    categories = ["Elektronik", "Fashion", "Makanan", "Kesehatan", "Olahraga", "Buku"]
    start = time.perf_counter()
    for cat in categories * (sample_size // len(categories) + 1):
        db.search(Product.category == cat)
    elapsed = time.perf_counter() - start
    return elapsed


def run_benchmark(n_records: int):
    db = get_db()
    products = generate_products(n_records)

    write_time = benchmark_write(db, products)
    read_time = benchmark_read(db, sample_size=100)

    db.close()

    result = {
        "database": "TinyDB (NoSQL)",
        "n_records": n_records,
        "write_time_sec": round(write_time, 4),
        "write_throughput_ops": round(n_records / write_time, 2),
        "read_time_sec": round(read_time, 4),
        "read_throughput_ops": round(100 / read_time, 2),
    }
    return result


if __name__ == "__main__":
    for n in [100, 1000, 5000]:
        print(run_benchmark(n))
