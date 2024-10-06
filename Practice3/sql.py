import time
import random
from datetime import date, timedelta

import psycopg2
from psycopg2.extras import execute_values

connection = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port=5432
)

def create_table():
    query = """
    DROP TABLE IF EXISTS sells;
    CREATE TABLE IF NOT EXISTS sells (
      id INT PRIMARY KEY,
      time DATE NOT NULL,
      product_id INT NOT NULL,
      store_id INT NOT NULL,
      quantity INT NOT NULL
    );
    
    DROP TABLE IF EXISTS products;
    CREATE TABLE IF NOT EXISTS products (
        product_id INT PRIMARY KEY,
        price DECIMAL(10, 2) NOT NULL
    );
    """

    start_time = time.time()
    with connection.cursor() as cursor:
        cursor.execute(query)
    connection.commit()

    end_time = time.time()
    print(f"0. Create tables SQL completed in {end_time - start_time}")

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
            # print(f"Inserted sells {total_inserted} records...")
            batch = []

    if batch:
        insert_batch(batch)
        total_inserted += len(batch)
        # print(f"Inserted sells {total_inserted} records...")

    print(f"0. Insertion sells completed SQL all {count} by chunk {batch_size} in {sells_time}")

    start_time = time.time()
    products = [(i, round(random.uniform(5.0, 500.0), 2)) for i in range(1, 51)]
    query = """
    INSERT INTO products (product_id, price) VALUES %s ON CONFLICT (product_id) DO NOTHING;
    """

    with connection.cursor() as cursor:
        execute_values(cursor, query, products)
    connection.commit()
    end_time = time.time()
    print(f"0. Insertion products completed SQL in {end_time - start_time}")
    print("-------------")


def insert_batch(batch):
    query = """
    INSERT INTO sells (id, time, product_id, store_id, quantity) VALUES %s;
    """
    start_time = time.time()
    try:
        with connection.cursor() as cursor:
            execute_values(cursor, query, batch)
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error inserting batch: {e}")
    end_time = time.time()
    return end_time - start_time

# Порахувати кількість проданого товару
def count_product_sold(product_id: int = None):
    if product_id:
        query = """
        SELECT SUM(quantity) FROM sells WHERE product_id = %s;
        """
    else:
        query = """
        SELECT SUM(quantity) FROM sells;
        """

    start_time = time.time()
    with connection.cursor() as cursor:
        cursor.execute(query, (product_id,))
        # print(f"Result {cursor.fetchone()}")

    end_time = time.time()
    if product_id:
        print(f"1. Count product id {product_id} sold SQL completed in {end_time - start_time}")
    else:
        print(f"1. Count all products sold SQL completed in {end_time - start_time}")
    print("---------")

# Порахувати вартість проданого товару
def count_product_price(product_id: int = None):
    if product_id:
        query = """
        SELECT SUM(s.quantity * p.price) FROM sells s JOIN products p ON s.product_id = p.product_id WHERE s.product_id = %s;
        """
    else:
        query = """
        SELECT SUM(s.quantity * p.price) FROM sells s JOIN products p ON s.product_id = p.product_id;
        """

    start_time = time.time()
    with connection.cursor() as cursor:
        cursor.execute(query, (product_id,))
        # print(f"Result {cursor.fetchone()}")

    end_time = time.time()
    if product_id:
        print(f"2. Count product id {product_id} price SQL completed in {end_time - start_time}")
    else:
        print(f"2. Count all products price SQL completed in {end_time - start_time}")
    print("---------")

# Порахувати вартість проданого товару за період
def count_product_price_period(product_id: int = None, start_date: date = None, end_date: date = None):
    if product_id:
        query = """
        SELECT SUM(s.quantity * p.price) FROM sells s JOIN products p ON s.product_id = p.product_id WHERE s.product_id = %s AND s.time >= %s AND s.time <= %s;
        """
    else:
        query = """
        SELECT SUM(s.quantity * p.price) FROM sells s JOIN products p ON s.product_id = p.product_id WHERE s.time >= %s AND s.time <= %s;
        """

    start_time = time.time()
    with connection.cursor() as cursor:
        if product_id:
            cursor.execute(query, (product_id, start_date, end_date))
        else:
            cursor.execute(query, (start_date, end_date))
        # print(f"Result {cursor.fetchone()}")

    end_time = time.time()
    if product_id:
        print(f"3. Count product id {product_id} price period SQL completed in {end_time - start_time}")
    else:
        print(f"3. Count all products price period SQL completed in {end_time - start_time}")
    print("---------")


# Порахувати скільки було придбано товару А в мазазині В за період С
def count_product_sold_period(product_id: int, store_id: int, start_date: date, end_date: date):
    query = """
    SELECT SUM(quantity) FROM sells WHERE product_id = %s AND store_id = %s AND time >= %s AND time <= %s;
    """

    start_time = time.time()
    with connection.cursor() as cursor:
        cursor.execute(query, (product_id, store_id, start_date, end_date))
        # print(f"Result {cursor.fetchone()}")

    end_time = time.time()
    print(f"4. Count product id {product_id} sold in store {store_id} period SQL completed in {end_time - start_time}")
    print("---------")

# Порахувати скільки було придбано товару А в усіх магазинах за період С
def count_product_sold_period_all_stores(product_id: int, start_date: date, end_date: date):
    query = """
    SELECT SUM(quantity) FROM sells WHERE product_id = %s AND time >= %s AND time <= %s;
    """

    start_time = time.time()
    with connection.cursor() as cursor:
        cursor.execute(query, (product_id, start_date, end_date))
        # print(f"Result {cursor.fetchone()}")

    end_time = time.time()
    print(f"5. Count product id {product_id} sold in all stores period SQL completed in {end_time - start_time}")
    print("---------")

# Порахувати сумарну виручку магазинів за період С
def count_store_revenue_period(start_date: date, end_date: date):
    query = """
    SELECT SUM(s.quantity * p.price) FROM sells s JOIN products p ON s.product_id = p.product_id WHERE s.time >= %s AND s.time <= %s;
    """

    start_time = time.time()
    with connection.cursor() as cursor:
        cursor.execute(query, (start_date, end_date))
        # print(f"Result {cursor.fetchone()}")

    end_time = time.time()
    print(f"6. Count store revenue period SQL completed in {end_time - start_time}")
    print("---------")

# Вивести топ 10 купівель товарів, де результатом буде рядок з двома продуктами
def count_top_10_products_period_pair(start_date: date, end_date: date, top: int = 10):
    query = f"""
    WITH grouped_sales AS (
        SELECT store_id, time, ARRAY_AGG(product_id) AS products
        FROM sells
        WHERE time BETWEEN %s AND %s
        GROUP BY store_id, time
    ), product_pairs AS (
        SELECT
            LEAST(p1, p2) AS product_one,
            GREATEST(p1, p2) AS product_two
        FROM grouped_sales,
        LATERAL (
            SELECT p1, p2
            FROM unnest(products) AS p1
            JOIN unnest(products) AS p2
              ON p1 < p2
        ) AS pair
    )
    SELECT 
        p1.product_id AS productOne, 
        p2.product_id AS productTwo, 
        COUNT(*) AS count
    FROM product_pairs pp
    JOIN products p1 ON pp.product_one = p1.product_id
    JOIN products p2 ON pp.product_two = p2.product_id
    GROUP BY p1.product_id, p2.product_id
    ORDER BY count DESC
    LIMIT %s;
    """

    start_time = time.time()
    with connection.cursor() as cursor:
        cursor.execute(query, (start_date, end_date, top))

    end_time = time.time()
    print(f"7. Top {top} product pairs sold between {start_date} and {end_date} SQL completed in {end_time - start_time:.4f} seconds")
    print("---------")

# * Вивести топ 10 купівель товарів по три за період С (наприклад молоко, масло, хліб - 1000 разів)
def count_top_10_products_period_triple(start_date: date, end_date: date, top: int = 10):
    query = f"""
    WITH grouped_sales AS (
        SELECT store_id, time, ARRAY_AGG(product_id) AS products
        FROM sells
        WHERE time BETWEEN %s AND %s
        GROUP BY store_id, time
    ), product_triples AS (
        SELECT
            LEAST(p1, p2, p3) AS product_one,
            LEAST(GREATEST(p1, p2), GREATEST(p1, p3), GREATEST(p2, p3)) AS product_two,
            GREATEST(p1, p2, p3) AS product_three
        FROM grouped_sales,
        LATERAL (
            SELECT p1, p2, p3
            FROM unnest(products) AS p1
            JOIN unnest(products) AS p2
              ON p1 < p2
            JOIN unnest(products) AS p3
              ON p2 < p3
        ) AS triple
    )
    SELECT 
        p1.product_id AS productOne, 
        p2.product_id AS productTwo, 
        p3.product_id AS productThree, 
        COUNT(*) AS count
    FROM product_triples pp
    JOIN products p1 ON pp.product_one = p1.product_id
    JOIN products p2 ON pp.product_two = p2.product_id
    JOIN products p3 ON pp.product_three = p3.product_id
    GROUP BY p1.product_id, p2.product_id, p3.product_id
    ORDER BY count DESC
    LIMIT %s;
    """

    start_time = time.time()
    with connection.cursor() as cursor:
        cursor.execute(query, (start_date, end_date, top))

    end_time = time.time()
    print(f"8. Top {top} product triples sold between {start_date} and {end_date} SQL completed in {end_time - start_time:.4f} seconds")
    print("---------")

# Вивести топ 10 купівель товарів по чотири за період С
def count_top_10_products_period_quadruple(start_date: date, end_date: date, top: int = 10):
    query = f"""
    WITH grouped_sales AS (
        SELECT store_id, time, ARRAY_AGG(product_id) AS products
        FROM sells
        WHERE time BETWEEN %s AND %s
        GROUP BY store_id, time
    ), product_quadruples AS (
        SELECT
            LEAST(p1, p2, p3, p4) AS product_one,
            LEAST(GREATEST(p1, p2, p3), GREATEST(p1, p2, p4), GREATEST(p1, p3, p4), GREATEST(p2, p3, p4)) AS product_two,
            LEAST(GREATEST(p1, p2, p3), GREATEST(p1, p2, p4), GREATEST(p1, p3, p4), GREATEST(p2, p3, p4)) AS product_three,
            GREATEST(p1, p2, p3, p4) AS product_four
        FROM grouped_sales,
        LATERAL (
            SELECT p1, p2, p3, p4
            FROM unnest(products) AS p1
            JOIN unnest(products) AS p2
              ON p1 < p2
            JOIN unnest(products) AS p3
              ON p2 < p3
            JOIN unnest(products) AS p4
              ON p3 < p4
        ) AS quadruple
    )
    SELECT 
        p1.product_id AS productOne, 
        p2.product_id AS productTwo, 
        p3.product_id AS productThree, 
        p4.product_id AS productFour, 
        COUNT(*) AS count
    FROM product_quadruples pp
    JOIN products p1 ON pp.product_one = p1.product_id
    JOIN products p2 ON pp.product_two = p2.product_id
    JOIN products p3 ON pp.product_three = p3.product_id
    JOIN products p4 ON pp.product_four = p4.product_id
    GROUP BY p1.product_id, p2.product_id, p3.product_id, p4.product_id
    ORDER BY count DESC
    LIMIT %s;
    """

    start_time = time.time()
    with connection.cursor() as cursor:
        cursor.execute(query, (start_date, end_date, top))

    end_time = time.time()
    print(f"9. Top {top} product quadruples sold between {start_date} and {end_date} SQL completed in {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    count_sells = 100_000
    batch_size = 1_000

    print("SQL by " + str(count_sells) + " sells")
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

    count_top_10_products_period_pair(date(2022, 1, 1), date(2023, 12, 31))
    count_top_10_products_period_triple(date(2022, 1, 1), date(2023, 12, 31))
    count_top_10_products_period_quadruple(date(2022, 1, 1), date(2023, 12, 31))

    connection.close()
