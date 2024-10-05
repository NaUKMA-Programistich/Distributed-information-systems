// забрати рюзюме з іменем, прізвищем, телефоном та роком народження
MATCH (user:User)-[:HAS_RESUME]->(resume:Resume)
RETURN resume.id AS ResumeID, resume.title AS Title, resume.content AS Content, user.first_name AS First, user.last_name AS Last, user.phone AS Phone, user.birth_year AS Birth;

// забрати всі резюме
MATCH (resume:Resume)
RETURN resume.id AS ID, resume.title AS Title, resume.content AS Content;

// забрати всі хоббі які існують в резюме
MATCH (user:User)-[:HAS_RESUME]->(:Resume), (user)-[:HAS_HOBBY]->(hobby:Hobby)
RETURN DISTINCT hobby.name AS Hobby;

// забрати всі міста, що зустрічаються в резюме
MATCH (user:User)-[:HAS_RESUME]->(:Resume)
RETURN DISTINCT user.city AS City;

// забрати хоббі всіх здобувачів, що мешкають в заданому місті
MATCH (user:User {city: 'Kyiv'})-[:HAS_HOBBY]->(hobby:Hobby)
RETURN hobby.name AS Hobby;

// забрати всіх здобувачів, що працювали в одному закладі (заклад ми не вказуємо)
MATCH (userOne:User)-[:WORKED_AT]->(institution:Institution)<-[:WORKED_AT]-(userTwo:User)
WHERE userOne.id < userTwo.id
UNWIND [userOne, userTwo] AS user
RETURN DISTINCT user.first_name + ' ' + user.last_name AS Name, institution.name;
