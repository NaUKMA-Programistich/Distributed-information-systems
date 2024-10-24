1. Created docker compose file with master and slave nodes
2. Run docker compose up
3. Go to node 1 ```psql -U postgres``` with password ```password```
   * ```CREATE ROLE slave_user WITH REPLICATION PASSWORD 'slave_password' LOGIN;```
   * ```CREATE TABLE test_table (id SERIAL PRIMARY KEY, data TEXT); CREATE PUBLICATION my_pub FOR TABLE test_table;```
   * ```CREATE SUBSCRIPTION my_sub_node2 CONNECTION 'host=postgres-node2 port=5432 dbname=database user=slave_user password=slave_password' PUBLICATION my_pub WITH (copy_data = false);```
   * ```ALTER SEQUENCE test_table_id_seq RESTART WITH 1 INCREMENT BY 2;```
4. Go to node 2 ```psql -U postgres``` with password ```password```
   * ```CREATE ROLE slave_user WITH REPLICATION PASSWORD 'slave_password' LOGIN;```
   * ```CREATE TABLE test_table (id SERIAL PRIMARY KEY, data TEXT); CREATE PUBLICATION my_pub FOR TABLE test_table;```
   * ```CREATE SUBSCRIPTION my_sub_node1 CONNECTION 'host=postgres-node1 port=5432 dbname=database user=slave_user password=slave_password' PUBLICATION my_pub WITH (copy_data = false);```
   * ```ALTER SEQUENCE test_table_id_seq RESTART WITH 2 INCREMENT BY 2;```
