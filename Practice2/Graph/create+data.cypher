CREATE (:User {id: 1, login: 'ale123', password: 'password123', first_name: 'Alex', last_name: 'Dzhos', birth_year: 2003, phone: '+12333', city: 'Lviv'});
CREATE (:User {id: 2, login: 'test', password: 'qwerty456', first_name: 'Test', last_name: 'Admin', birth_year: 2500, phone: '+424242424', city: 'Kyiv'});
CREATE (:User {id: 3, login: 'admin', password: 'admin', first_name: 'Admin', last_name: 'Admin', birth_year: 1999, phone: '+123456789', city: 'Lviv'});
CREATE (:User {id: 4, login: 'olena228', password: 'securepass', first_name: 'Olena', last_name: 'Koval', birth_year: 1999, phone: '+380123456789', city: 'Warsaw'});
CREATE (:User {id: 5, login: 'troshab', password: 'daflkdkayduakdladhjlaid', first_name: 'Bohdan', last_name: 'Trosh', birth_year: 1999, phone: '+380123456789', city: 'LvivX'});

CREATE (:Hobby {id: 1, name: 'Football'});
CREATE (:Hobby {id: 2, name: 'Basketball'});
CREATE (:Hobby {id: 3, name: 'Volleyball'});
CREATE (:Hobby {id: 4, name: 'Tennis'});
CREATE (:Hobby {id: 5, name: 'Swimming'});
CREATE (:Hobby {id: 6, name: 'Running'});
CREATE (:Hobby {id: 7, name: 'Cycling'});
CREATE (:Hobby {id: 8, name: 'Gym'});
CREATE (:Hobby {id: 9, name: 'Yoga'});
CREATE (:Hobby {id: 10, name: 'Pilates'});

UNWIND [
    {user_id: 1, hobby_id: 1},
    {user_id: 1, hobby_id: 2},
    {user_id: 1, hobby_id: 3},
    {user_id: 1, hobby_id: 4},
    {user_id: 1, hobby_id: 5},
    {user_id: 1, hobby_id: 6},
    {user_id: 1, hobby_id: 7},
    {user_id: 1, hobby_id: 8},
    {user_id: 2, hobby_id: 7},
    {user_id: 2, hobby_id: 8},
    {user_id: 3, hobby_id: 1},
    {user_id: 3, hobby_id: 2},
    {user_id: 3, hobby_id: 3},
    {user_id: 3, hobby_id: 4},
    {user_id: 3, hobby_id: 5},
    {user_id: 3, hobby_id: 6},
    {user_id: 3, hobby_id: 7},
    {user_id: 3, hobby_id: 8},
    {user_id: 4, hobby_id: 1},
    {user_id: 4, hobby_id: 2},
    {user_id: 4, hobby_id: 3},
    {user_id: 4, hobby_id: 4},
    {user_id: 4, hobby_id: 5},
    {user_id: 4, hobby_id: 6},
    {user_id: 4, hobby_id: 7},
    {user_id: 4, hobby_id: 8},
    {user_id: 4, hobby_id: 9},
    {user_id: 5, hobby_id: 1},
    {user_id: 5, hobby_id: 2},
    {user_id: 5, hobby_id: 3},
    {user_id: 5, hobby_id: 4},
    {user_id: 5, hobby_id: 5},
    {user_id: 5, hobby_id: 6},
    {user_id: 5, hobby_id: 7},
    {user_id: 5, hobby_id: 8},
    {user_id: 5, hobby_id: 10}
] AS entry
MATCH (u:User {id: entry.user_id}), (h:Hobby {id: entry.hobby_id})
CREATE (u)-[:HAS_HOBBY]->(h);

CREATE (:Resume {id: 1, title: 'Junior Java Developer', content: 'I am a junior java developer'});
CREATE (:Resume {id: 2, title: 'Junior Kotlin Developer', content: 'I am a junior kotlin developer'});
CREATE (:Resume {id: 3, title: 'Junior Android Developer', content: 'I am a junior android developer'});
CREATE (:Resume {id: 4, title: 'Senior Java Developer', content: 'I am a senior java developer'});
CREATE (:Resume {id: 5, title: 'Middle Java Developer, Team Lead', content: 'I am a middle java developer and team lead'});
CREATE (:Resume {id: 6, title: 'Middle Java Developer', content: 'I am a middle java developer'});

UNWIND [
    {user_id: 1, resume_id: 1},
    {user_id: 1, resume_id: 2},
    {user_id: 1, resume_id: 3},
    {user_id: 2, resume_id: 4},
    {user_id: 3, resume_id: 5},
    {user_id: 4, resume_id: 6}
] AS entry
MATCH (u:User {id: entry.user_id}), (r:Resume {id: entry.resume_id})
CREATE (u)-[:HAS_RESUME]->(r);

CREATE (:Institution {id: 1, name: 'SoftServe'});
CREATE (:Institution {id: 2, name: 'Google'});
CREATE (:Institution {id: 3, name: 'Facebook'});
CREATE (:Institution {id: 4, name: 'Microsoft'});
CREATE (:Institution {id: 5, name: 'Apple'});
CREATE (:Institution {id: 6, name: 'Amazon'});

UNWIND [
    {user_id: 1, institution_id: 1},
    {user_id: 1, institution_id: 2},
    {user_id: 1, institution_id: 3},
    {user_id: 2, institution_id: 4},
    {user_id: 2, institution_id: 2},
    {user_id: 3, institution_id: 5},
    {user_id: 4, institution_id: 6},
    {user_id: 5, institution_id: 3}
] AS entry
MATCH (u:User {id: entry.user_id}), (i:Institution {id: entry.institution_id})
CREATE (u)-[:WORKED_AT]->(i);
