import psycopg2

master = {'host': '127.0.0.1', 'port': '5433', 'dbname': 'database', 'user': 'postgres', 'password': 'password' }
slave = {'host': '127.0.0.1', 'port': '5434', 'dbname': 'database', 'user': 'slave_user', 'password': 'slave_password'}

def write_to_master():
    try:
        with psycopg2.connect(**master) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS test_table (
                        id SERIAL PRIMARY KEY,
                        data TEXT
                    );
                """)
                cursor.execute("INSERT INTO test_table (data) VALUES (%s)", ("Test data",))
                conn.commit()
                print("Data written to master node.")
    except Exception as e:
        print(f"Error writing to master: {e}")

def read_from_slave():
    try:
        with psycopg2.connect(**slave) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM test_table;")
                rows = cur.fetchall()
                print("Data read from slave node:")
                for row in rows:
                    print(row)
    except Exception as e:
        print(f"Error reading from slave: {e}")

if __name__ == "__main__":
    write_to_master()
    read_from_slave()
