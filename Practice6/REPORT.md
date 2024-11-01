1. Create table
```sql
CREATE TABLE users (
    id SERIAL,
    name TEXT NOT NULL,
    email TEXT,
    PRIMARY KEY (id, name)
) PARTITION BY HASH (name)
```

2. Create partitions
```sql
CREATE TABLE users_part_0 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE users_part_1 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE users_part_2 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE users_part_3 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 3);
```

3. Insert data
```sql
INSERT INTO users (name, email) VALUES ('Test', 'test@gmail.com');
INSERT INTO users (name, email) VALUES ('Alex', 'alex@icloud.com');
INSERT INTO users (name, email) VALUES ('Denis', 'denis@mail.com');
INSERT INTO users (name, email) VALUES ('Olga', 'olga@gmail.com');
INSERT INTO users (name, email) VALUES ('Ivan', 'ivan@mail.com');
INSERT INTO users (name, email) VALUES ('Vlad', 'vlad_test@gmail.com');
```

4. Select data
```sql
SELECT * FROM users_part_0;
SELECT * FROM users_part_1;
SELECT * FROM users_part_2;
SELECT * FROM users_part_3;
```