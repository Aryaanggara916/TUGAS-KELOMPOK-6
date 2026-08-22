"""
benchmark_sql.py
------------------
Mengukur kinerja database SQL/relasional untuk skenario data transaksi
(orders) pada sistem e-commerce, menggunakan SQLite.

Catatan: SQLite dipilih sebagai representasi database SQL karena tidak
memerlukan instalasi server terpisah (built-in di Python), namun tetap
merepresentasikan karakteristik inti SQL: skema tetap, tipe data ketat,
dan transaksi ACID -- sehingga hasil analisis kinerja tetap valid untuk
dibandingkan dengan NoSQL dan In-Memory Database.

Metrik yang diukur:
- Write latency & throughput (INSERT)
- Read latency & throughput (SELECT dengan kondisi WHERE)
"""

import os
import time
import sqlite3
from generate_data import generate_orders

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "orders.db")


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def setup_table(conn):
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS orders;")
    cur.execute("""
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            total_price REAL NOT NULL,
            status TEXT NOT NULL
        );
    """)
    conn.commit()


def benchmark_write(conn, orders):
    cur = conn.cursor()
    start = time.perf_counter()
    cur.executemany(
        """INSERT INTO orders (order_id, user_id, product_id, quantity, total_price, status)
           VALUES (?, ?, ?, ?, ?, ?)""",
        [(o["order_id"], o["user_id"], o["product_id"], o["quantity"], o["total_price"], o["status"])
         for o in orders],
    )
    conn.commit()
    elapsed = time.perf_counter() - start
    return elapsed


def benchmark_read(conn, sample_size=100):
    cur = conn.cursor()
    start = time.perf_counter()
    for status in ["pending", "paid", "shipped", "completed"] * (sample_size // 4 + 1):
        cur.execute("SELECT * FROM orders WHERE status = ? LIMIT 50;", (status,))
        cur.fetchall()
    elapsed = time.perf_counter() - start
    return elapsed


def run_benchmark(n_records: int):
    conn = get_connection()
    setup_table(conn)
    orders = generate_orders(n_records)

    write_time = benchmark_write(conn, orders)
    read_time = benchmark_read(conn, sample_size=100)

    conn.close()

    result = {
        "database": "SQLite (SQL)",
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
