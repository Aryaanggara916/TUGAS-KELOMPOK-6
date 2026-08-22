"""
run_all_benchmarks.py
-----------------------
Script utama proyek "Evaluasi Kinerja Database SQL, NoSQL, dan In-Memory
pada Sistem E-Commerce". Menjalankan benchmark PostgreSQL, MongoDB, dan
Redis pada beberapa volume data, lalu menyimpan hasilnya dalam bentuk
CSV dan grafik perbandingan (PNG) di folder results/.

Cara pakai:
    1. Pastikan docker-compose sudah jalan (lihat README.md)
    2. pip install -r requirements.txt
    3. python scripts/run_all_benchmarks.py
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate

sys.path.append(os.path.dirname(__file__))

import benchmark_sql
import benchmark_nosql
import benchmark_inmemory

VOLUMES = [100, 1000, 5000]
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")


def run_all():
    all_results = []

    print("=== Menjalankan benchmark SQLite (SQL) ===")
    for n in VOLUMES:
        all_results.append(benchmark_sql.run_benchmark(n))

    print("=== Menjalankan benchmark TinyDB (NoSQL) ===")
    for n in VOLUMES:
        all_results.append(benchmark_nosql.run_benchmark(n))

    print("=== Menjalankan benchmark fakeredis (In-Memory) ===")
    for n in VOLUMES:
        all_results.append(benchmark_inmemory.run_benchmark(n))

    return pd.DataFrame(all_results)


def save_results(df: pd.DataFrame):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    csv_path = os.path.join(RESULTS_DIR, "comparison_results.csv")
    df.to_csv(csv_path, index=False)
    print(f"\nHasil tersimpan di: {csv_path}")
    return csv_path


def plot_results(df: pd.DataFrame):
    os.makedirs(RESULTS_DIR, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    for db_name, group in df.groupby("database"):
        axes[0].plot(group["n_records"], group["write_throughput_ops"], marker="o", label=db_name)
        axes[1].plot(group["n_records"], group["read_throughput_ops"], marker="o", label=db_name)

    axes[0].set_title("Perbandingan Write Throughput")
    axes[0].set_xlabel("Jumlah Record")
    axes[0].set_ylabel("Operasi / detik")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].set_title("Perbandingan Read Throughput")
    axes[1].set_xlabel("Jumlah Record")
    axes[1].set_ylabel("Operasi / detik")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    png_path = os.path.join(RESULTS_DIR, "throughput_comparison.png")
    plt.savefig(png_path, dpi=150)
    print(f"Grafik tersimpan di: {png_path}")
    return png_path


def print_summary(df: pd.DataFrame):
    print("\n=== RINGKASAN HASIL BENCHMARK ===")
    print(tabulate(df, headers="keys", tablefmt="grid", showindex=False))


if __name__ == "__main__":
    df = run_all()
    print_summary(df)
    save_results(df)
    plot_results(df)
