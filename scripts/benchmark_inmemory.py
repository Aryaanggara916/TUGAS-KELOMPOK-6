"""
benchmark_inmemory.py
------------------------
Mengukur kinerja In-Memory Database untuk skenario keranjang belanja
(cart) & session pada sistem e-commerce, menggunakan fakeredis.

Catatan: fakeredis dipilih sebagai representasi In-Memory Database
karena mengimplementasikan API Redis secara penuh murni di dalam
Python (tanpa perlu instalasi server Redis terpisah), sehingga
karakteristik inti In-Memory DB tetap terjaga: penyimpanan di RAM
dan struktur data key-value/hash yang sangat cepat diakses --
hasil analisis kinerja tetap valid untuk dibandingkan dengan SQL
dan NoSQL.

Metrik yang diukur:
- Write latency & throughput (HSET per cart item)
- Read latency & throughput (HGETALL per cart item)
"""

import time
import fakeredis
from generate_data import generate_cart_items


def get_client():
    return fakeredis.FakeStrictRedis(decode_responses=True)


def setup(client):
    client.flushdb()


def benchmark_write(client, cart_items):
    start = time.perf_counter()
    pipe = client.pipeline()
    for item in cart_items:
        pipe.hset(item["cart_id"], mapping={
            "user_id": item["user_id"],
            "product_id": item["product_id"],
            "quantity": item["quantity"],
        })
    pipe.execute()
    elapsed = time.perf_counter() - start
    return elapsed


def benchmark_read(client, cart_items, sample_size=100):
    sample = cart_items[:sample_size] if len(cart_items) >= sample_size else cart_items
    start = time.perf_counter()
    for item in sample:
        client.hgetall(item["cart_id"])
    elapsed = time.perf_counter() - start
    return elapsed


def run_benchmark(n_records: int):
    client = get_client()
    setup(client)
    cart_items = generate_cart_items(n_records)

    write_time = benchmark_write(client, cart_items)
    read_time = benchmark_read(client, cart_items, sample_size=100)

    result = {
        "database": "fakeredis (In-Memory)",
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
