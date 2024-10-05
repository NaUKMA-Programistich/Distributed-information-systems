INSERT INTO users (login, password) VALUES
('ale123', 'password123'),
('test', 'qwerty456'),
('admin', 'admin'),
('olena228', 'securepass'),
('troshab', 'daflkdkayduakdladhjlaid');


INSERT INTO profiles (user_id, first_name, last_name, birth_year, phone, city) VALUES
(1, 'Alex', 'Dzhos', 2003, '+12333', 'Lviv'),
(2, 'Test', 'Admin', 2500, '+424242424', 'Kyiv'),
(3, 'Admin', 'Admin', 1999, '+123456789', 'Lviv'),
(4, 'Olena', 'Koval', 1999, '+380123456789', 'Warsaw'),
(5, 'Bohdan', 'Trosh', 1999, '+380123456789', 'LvivX');

INSERT INTO hobbies (name) VALUES
('Football'), -- 1
('Basketball'), -- 2
('Volleyball'), -- 3
('Tennis'), -- 4
('Swimming'), -- 5
('Running'), -- 6
('Cycling'), -- 7
('Gym'), -- 8
('Yoga'), -- 9
('Pilates'); -- 10 empty

INSERT INTO resumes (user_id, title, content) VALUES
(1, 'Junior Java Developer', 'I am a junior java developer'),
(1, 'Junior Kotlin Developer', 'I am a junior kotlin developer'),
(1, 'Junior Android Developer', 'I am a junior android developer'),
(2, 'Senior Java Developer', 'I am a senior java developer'),
(3, 'Middle Java Developer, Team Lead', 'I am a middle java developer and team lead'),
(4, 'Middle Java Developer', 'I am a middle java developer');

INSERT INTO users_hobbies (user_id, hobby_id) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 5),
(1, 6),
(1, 7),
(1, 8),
(2, 7),
(2, 8),
(3, 1),
(3, 2),
(3, 3),
(3, 4),
(3, 5),
(3, 6),
(3, 7),
(3, 8),
(4, 1),
(4, 2),
(4, 3),
(4, 4),
(4, 5),
(4, 6),
(4, 7),
(4, 8),
(4, 9),
(5, 1),
(5, 2),
(5, 3),
(5, 4),
(5, 5),
(5, 6),
(5, 7),
(5, 8),
(5, 10);

INSERT INTO experiences (user_id, institution) VALUES
(1, 'SoftServe'),
(1, 'Google'),
(1, 'Facebook'),
(2, 'Microsoft'),
(2, 'Google'),
(3, 'Apple'),
(4, 'Amazon'),
(5, 'Facebook');