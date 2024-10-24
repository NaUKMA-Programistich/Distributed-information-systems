1. Created docker compose file with master and slave nodes
2. Run docker compose up
3. Create user on master for slave ```psql -U postgres``` with password ```password```
```sql
CREATE USER slave_user WITH PASSWORD 'slave_password';
GRANT CONNECT ON DATABASE database TO slave_user;
\connect database
GRANT SELECT ON ALL TABLES IN SCHEMA public TO slave_user;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO slave_user;
GRANT USAGE ON SCHEMA public TO slave_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO slave_user;
```
4. Create database on master with insert data
5. Read data from slave