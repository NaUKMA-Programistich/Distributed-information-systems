import psycopg2
import time

master_node_one = {'host': '127.0.0.1', 'port': '5435', 'dbname': 'database', 'user': 'postgres', 'password': 'postgres' }
master_node_two = {'host': '127.0.0.1', 'port': '5436', 'dbname': 'database', 'user': 'postgres', 'password': 'postgres' }

def write_to_master_node_one():
    try:
        with psycopg2.connect(**master_node_one) as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO test_table (data) VALUES (%s)", ("Test data from node1",))
                conn.commit()
                print("Data written to master node 1.")
    except Exception as e:
        print(f"Error writing to master node 1: {e}")


def write_to_master_node_two():
    try:
        with psycopg2.connect(**master_node_two) as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO test_table (data) VALUES (%s)", ("Test data from node2",))
                conn.commit()
                print("Data written to master node 2.")
    except Exception as e:
        print(f"Error writing to master node 2: {e}")


def read_from_master_node_one():
    try:
        with psycopg2.connect(**master_node_one) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM test_table;")
                rows = cur.fetchall()
                print("Data read from master node 1:")
                for row in rows:
                    print(row)
    except Exception as e:
        print(f"Error reading from master node 1: {e}")


def read_from_master_node_two():
    try:
        with psycopg2.connect(**master_node_two) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM test_table;")
                rows = cur.fetchall()
                print("Data read from master node 2:")
                for row in rows:
                    print(row)
    except Exception as e:
        print(f"Error reading from master node 2: {e}")


if __name__ == "__main__":
    write_to_master_node_one()
    write_to_master_node_two()

    time.sleep(5)

    read_from_master_node_one()
    read_from_master_node_two()
