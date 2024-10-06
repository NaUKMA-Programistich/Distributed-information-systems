import time
import random
from collections import Counter
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from itertools import combinations

from clickhouse_driver import Client

client = Client(host='localhost', port=9001, database='default')

def create_table():
    client.execute("""DROP TABLE IF EXISTS sells""")
    client.execute("""DROP TABLE IF EXISTS products""")

    start_time = time.time()
    client.execute("""
        CREATE TABLE IF NOT EXISTS sells (
          id Int32,
          time Date,
          product_id Int32,
          store_id Int32,
          quantity Int32,
          PRIMARY KEY (id)
        ) ENGINE = MergeTree()
        ORDER BY (id);
        """
    )

    client.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id Int32,
            price Decimal(10, 2),
            PRIMARY KEY (product_id)
            ) ENGINE = MergeTree()
    """)

    end_time = time.time()
    print(f"0. Create tables ClickHouse completed in {end_time - start_time}")


def generate_random_sell(sell_id) -> dict:
    today = date.today()
    start_date = today - timedelta(days=365)
    random_number_of_days = random.randint(0, 365)

    sell_date = start_date + timedelta(days=random_number_of_days)
    product_id = random.randint(1, 50)
    store_id = random.randint(1, 10)
    quantity_sold = random.randint(1, 60)

    return {
        "id": sell_id,
        "time": sell_date,
        "product_id": product_id,
        "store_id": store_id,
        "quantity": quantity_sold
    }

def insert_sells(count: int = 1_000_000, batch_size: int = 10_000):
    sells_time = 0

    total_inserted = 0
    batch = []

    for sell_id in range(count):
        sell = generate_random_sell(sell_id)
        record = (
            sell["id"],
            sell["time"],
            sell["product_id"],
            sell["store_id"],
            sell["quantity"]
        )
        batch.append(record)

        if len(batch) >= batch_size:
            sells_time += insert_batch(batch)
            total_inserted += len(batch)
            batch = []

    if batch:
        insert_batch(batch)
        total_inserted += len(batch)

    print(f"0. Insertion sells completed ClickHouse all {count} by chunk {batch_size} in {sells_time}")

    products = []
    for i in range(1, 51):
        price = Decimal(random.uniform(5.0, 500.0)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        products.append((i, price))

    query = "INSERT INTO products (product_id, price) VALUES"

    start_time = time.time()
    client.execute(query, products)
    end_time = time.time()
    print(f"0. Insertion products completed ClickHouse in {end_time - start_time}")
    print("-------------")

def insert_batch(batch):
    query = "INSERT INTO sells (id, time, product_id, store_id, quantity) VALUES"
    start_time = time.time()
    try:
        client.execute(query, batch)
    except Exception as e:
        print(f"Error inserting batch: {e}")
    end_time = time.time()
    return end_time - start_time

# Порахувати кількість проданого товару
def count_product_sold(product_id: int = None):
    start_time = time.time()
    if product_id is not None:
        query = """
        SELECT SUM(quantity) FROM sells WHERE product_id = %(product_id)s;
        """
        params = {'product_id': product_id}
        result = client.execute(query, params)
    else:
        query = """
        SELECT SUM(quantity) FROM sells;
        """
        result = client.execute(query)
    end_time = time.time()
    if product_id is not None:
        print(f"1. Count product id {product_id} sold ClickHouse completed in {end_time - start_time} seconds")
    else:
        print(f"1. Count all products sold ClickHouse completed in {end_time - start_time} seconds")
    print("---------")

# Порахувати вартість проданого товару
def count_product_price(product_id: int = None):
    start_time = time.time()
    if product_id is not None:
        query = """
        SELECT SUM(s.quantity * p.price) FROM sells s JOIN products p ON s.product_id = p.product_id WHERE s.product_id = %(product_id)s;
        """
        params = {'product_id': product_id}
        result = client.execute(query, params)
    else:
        query = """
        SELECT SUM(s.quantity * p.price) FROM sells s JOIN products p ON s.product_id = p.product_id;
        """
        result = client.execute(query)
    end_time = time.time()
    if product_id is not None:
        print(f"2. Count product id {product_id} price ClickHouse completed in {end_time - start_time}")
    else:
        print(f"2. Count all products price ClickHouse completed in {end_time - start_time}")
    print("---------")

# Порахувати вартість проданого товару за період
def count_product_price_period(product_id: int = None, start_date: date = None, end_date: date = None):
    start_time = time.time()
    if product_id is not None:
        query = """
        SELECT SUM(s.quantity * p.price) FROM sells s JOIN products p ON s.product_id = p.product_id WHERE s.product_id = %(product_id)s AND s.time >= %(start_date)s AND s.time <= %(end_date)s;
        """
        params = {'product_id': product_id, 'start_date': start_date, 'end_date': end_date}
        result = client.execute(query, params)
    else:
        query = """
        SELECT SUM(s.quantity * p.price) FROM sells s JOIN products p ON s.product_id = p.product_id WHERE s.time >= %(start_date)s AND s.time <= %(end_date)s;
        """
        params = {'start_date': start_date, 'end_date': end_date}
        result = client.execute(query, params)
    end_time = time.time()
    if product_id is not None:
        print(f"3. Count product id {product_id} price period ClickHouse completed in {end_time - start_time}")
    else:
        print(f"3. Count all products price period ClickHouse completed in {end_time - start_time}")
    print("---------")

# # Порахувати скільки було придбано товару А в мазазині В за період С
def count_product_sold_period(product_id: int, store_id: int, start_date: date, end_date: date):
    start_time = time.time()
    query = """
    SELECT SUM(quantity) FROM sells WHERE product_id = %(product_id)s AND store_id = %(store_id)s AND time >= %(start_date)s AND time <= %(end_date)s;
    """
    params = {'product_id': product_id, 'store_id': store_id, 'start_date': start_date, 'end_date': end_date}
    result = client.execute(query, params)
    end_time = time.time()
    print(f"4. Count product id {product_id} sold in store {store_id} period ClickHouse completed in {end_time - start_time}")
    print("---------")

# # Порахувати скільки було придбано товару А в усіх магазинах за період С
def count_product_sold_period_all_stores(product_id: int, start_date: date, end_date: date):
    start_time = time.time()
    query = """
    SELECT SUM(quantity) FROM sells WHERE product_id = %(product_id)s AND time >= %(start_date)s AND time <= %(end_date)s;
    """
    params = {'product_id': product_id, 'start_date': start_date, 'end_date': end_date}
    result = client.execute(query, params)
    end_time = time.time()
    print(f"5. Count product id {product_id} sold in all stores period ClickHouse completed in {end_time - start_time}")
    print("---------")

# Порахувати сумарну виручку магазинів за період С
def count_store_revenue_period(start_date: date, end_date: date):
    start_time = time.time()
    query = """
    SELECT SUM(s.quantity * p.price) FROM sells s JOIN products p ON s.product_id = p.product_id WHERE s.time >= %(start_date)s AND s.time <= %(end_date)s;
    """
    params = {'start_date': start_date, 'end_date': end_date}
    result = client.execute(query, params)
    end_time = time.time()
    print(f"6. Count store revenue period ClickHouse completed in {end_time - start_time}")
    print("---------")

# Вивести топ 10 купівель товарів, де результатом буде рядок з 2/3/4 товарів
def count_top_10_products_period(start_date: date, end_date: date, count: int):
    start_time = time.time()

    query = """
        SELECT store_id, time, product_id
        FROM sells
        WHERE time BETWEEN %(start_date)s AND %(end_date)s
        ORDER BY store_id, time
    """
    data = client.execute(query, {'start_date': start_date, 'end_date': end_date})

    transactions = {}
    for store_id, txn_time, product_id in data:
        key = (store_id, txn_time)
        if key not in transactions:
            transactions[key] = set()
        transactions[key].add(product_id)

    pair_counter = Counter()
    for products in transactions.values():
        if len(products) < count:
            continue

        for pair in combinations(sorted(products), count):
            pair_counter[pair] += 1

    top_10 = pair_counter.most_common(10)

    end_time = time.time()
    print(f"7. Count top 10 products period ClickHouse completed in {end_time - start_time}")
    print("---------")

if __name__ == "__main__":
    count_sells = 100_000
    batch_size = 1_000

    print("Column by " + str(count_sells) + " sells")
    print("---------")

    create_table()
    insert_sells(count_sells, batch_size=batch_size)

    count_product_sold(product_id=3)
    count_product_sold()

    count_product_price(product_id=3)
    count_product_price()

    count_product_price_period(product_id=3, start_date=date(2022, 1, 1), end_date=date(2023, 12, 31))
    count_product_price_period(start_date=date(2022, 1, 1), end_date=date(2023, 12, 31))

    count_product_sold_period(3, 4, date(2022, 1, 1), date(2023, 12, 31))

    count_product_sold_period_all_stores(3, date(2022, 1, 1), date(2023, 12, 31))

    count_store_revenue_period(date(2022, 1, 1), date(2023, 12, 31))

    count_top_10_products_period(date(2022, 1, 1), date(2023, 12, 31), 2)
    count_top_10_products_period(date(2022, 1, 1), date(2023, 12, 31), 3)
    count_top_10_products_period(date(2022, 1, 1), date(2023, 12, 31), 4)
