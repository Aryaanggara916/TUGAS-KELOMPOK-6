"""
generate_data.py
-----------------
Menghasilkan data dummy untuk skenario e-commerce:
- Produk (katalog produk dengan atribut fleksibel -> cocok untuk NoSQL)
- Cart item (data sementara keranjang belanja -> cocok untuk In-Memory DB)
- Order (data transaksi terstruktur -> cocok untuk SQL relasional)

Data disimpan sebagai list of dict agar bisa dipakai ulang oleh
ketiga script benchmark (benchmark_postgres.py, benchmark_mongodb.py,
benchmark_redis.py) supaya perbandingannya adil (apple-to-apple).
"""

import random
from faker import Faker

fake = Faker("id_ID")

CATEGORIES = ["Elektronik", "Fashion", "Makanan", "Kesehatan", "Olahraga", "Buku"]


def generate_products(n: int):
    """Generate n data produk dengan skema yang bisa bervariasi (mensimulasikan
    keunggulan NoSQL dalam menangani skema fleksibel)."""
    products = []
    for i in range(n):
        product = {
            "product_id": i + 1,
            "name": fake.catch_phrase(),
            "category": random.choice(CATEGORIES),
            "price": round(random.uniform(10_000, 5_000_000), 2),
            "stock": random.randint(0, 500),
        }
        # Simulasi skema fleksibel: sebagian produk punya atribut tambahan
        if product["category"] == "Elektronik":
            product["specs"] = {
                "warranty_months": random.choice([6, 12, 24]),
                "power_watt": random.randint(5, 500),
            }
        elif product["category"] == "Fashion":
            product["variants"] = {
                "size": random.sample(["S", "M", "L", "XL"], k=random.randint(1, 3)),
                "color": fake.color_name(),
            }
        products.append(product)
    return products


def generate_cart_items(n: int):
    """Generate n data cart/session, cocok untuk In-Memory DB (Redis)
    karena sifatnya sementara dan butuh akses super cepat."""
    cart_items = []
    for i in range(n):
        cart_items.append({
            "cart_id": f"cart:{i+1}",
            "user_id": random.randint(1, n),
            "product_id": random.randint(1, n),
            "quantity": random.randint(1, 5),
        })
    return cart_items


def generate_orders(n: int):
    """Generate n data order/transaksi, cocok untuk SQL karena butuh
    konsistensi dan relasi antar tabel (ACID)."""
    orders = []
    for i in range(n):
        orders.append({
            "order_id": i + 1,
            "user_id": random.randint(1, n),
            "product_id": random.randint(1, n),
            "quantity": random.randint(1, 5),
            "total_price": round(random.uniform(10_000, 10_000_000), 2),
            "status": random.choice(["pending", "paid", "shipped", "completed"]),
        })
    return orders


if __name__ == "__main__":
    # Contoh penggunaan cepat / sanity check
    prods = generate_products(5)
    carts = generate_cart_items(5)
    orders = generate_orders(5)
    print("Contoh Produk:", prods[0])
    print("Contoh Cart Item:", carts[0])
    print("Contoh Order:", orders[0])
