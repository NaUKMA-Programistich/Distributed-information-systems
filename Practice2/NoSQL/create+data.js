db.hobbies.insertMany([
    { "name": "Football" },
    { "name": "Basketball" },
    { "name": "Volleyball" },
    { "name": "Tennis" },
    { "name": "Swimming" },
    { "name": "Running" },
    { "name": "Cycling" },
    { "name": "Gym" },
    { "name": "Yoga" },
    { "name": "Pilates" }
]);

const hobbiesMap = {};
db.hobbies.find().toArray().forEach(hobby => {
    hobbiesMap[hobby.name] = hobby._id;
});

db.users.insertMany([
    {
        "login": "ale123",
        "password": "password123",
        "profile": {
            "first_name": "Alex",
            "last_name": "Dzhos",
            "birth_year": 2003,
            "phone": "+12333",
            "city": "Lviv"
        },
        "hobbies": [
            hobbiesMap["Football"],
            hobbiesMap["Basketball"],
            hobbiesMap["Volleyball"],
            hobbiesMap["Tennis"],
            hobbiesMap["Swimming"],
            hobbiesMap["Running"],
            hobbiesMap["Cycling"],
            hobbiesMap["Gym"]
            ]
    },
    {
        "login": "test",
        "password": "qwerty456",
        "profile": {
            "first_name": "Test",
            "last_name": "Admin",
            "birth_year": 2500,
            "phone": "+424242424",
            "city": "Kyiv"
        },
        "hobbies": [
            hobbiesMap["Cycling"],
            hobbiesMap["Gym"],
            ]
    },
    {
        "login": "admin",
        "password": "admin",
        "profile": {
            "first_name": "Admin",
            "last_name": "Admin",
            "birth_year": 1999,
            "phone": "+123456789",
            "city": "Lviv"
        },
         "hobbies": [
            hobbiesMap["Football"],
            hobbiesMap["Basketball"],
            hobbiesMap["Volleyball"],
            hobbiesMap["Tennis"],
            hobbiesMap["Swimming"],
            hobbiesMap["Running"],
            hobbiesMap["Cycling"],
            hobbiesMap["Gym"]
            ]
    },
    {
        "login": "olena228",
        "password": "securepass",
        "profile": {
            "first_name": "Olena",
            "last_name": "Koval",
            "birth_year": 1999,
            "phone": "+380123456789",
            "city": "Warsaw"
        },
         "hobbies": [
            hobbiesMap["Football"],
            hobbiesMap["Basketball"],
            hobbiesMap["Volleyball"],
            hobbiesMap["Tennis"],
            hobbiesMap["Swimming"],
            hobbiesMap["Running"],
            hobbiesMap["Cycling"],
            hobbiesMap["Gym"],
            hobbiesMap["Yoga"],
            ]
    },
    {
        "login": "troshab",
        "password": "daflkdkayduakdladhjlaid",
        "profile": {
            "first_name": "Bohdan",
            "last_name": "Trosh",
            "birth_year": 1999,
            "phone": "+380123456789",
            "city": "LvivX"
        },
         "hobbies": [
            hobbiesMap["Football"],
            hobbiesMap["Basketball"],
            hobbiesMap["Volleyball"],
            hobbiesMap["Tennis"],
            hobbiesMap["Swimming"],
            hobbiesMap["Running"],
            hobbiesMap["Cycling"],
            hobbiesMap["Pilates"]
            ]
    }
]);

const usersId = db.users.find().toArray().map(user => user._id);

db.resumes.insertMany([
    {
        user_id: usersId[0],
        title: 'Junior Java Developer',
        content: 'I am a junior java developer'
    },
    {
        user_id: usersId[0],
        title: 'Junior Kotlin Developer',
        content: 'I am a junior kotlin developer'
    },
    {
        user_id: usersId[0],
        title: 'Junior Android Developer',
        content: 'I am a junior android developer'
    },
    {
        user_id: usersId[1],
        title: 'Senior Java Developer',
        content: 'I am a senior java developer'
    },
    {
        user_id: usersId[2],
        title: 'Middle Java Developer, Team Lead',
        content: 'I am a middle java developer and team lead'
    },
    {
        user_id: usersId[3],
        title: 'Middle Java Developer',
        content: 'I am a middle java developer'
    }
]);

db.experiences.insertMany([
    {
        user_id: usersId[0],
        institution: 'SoftServe',
    },
    {
        user_id: usersId[0],
        institution: 'Google',
    },
    {
        user_id: usersId[0],
        institution: 'Facebook',
    },
    {
        user_id: usersId[1],
        institution: 'Microsoft',
    },
    {
        user_id: usersId[1],
        institution: 'Google',
    },
    {
        user_id: usersId[2],
        institution: 'Apple',
    },
    {
        user_id: usersId[3],
        institution: 'Amazon',
    },
    {
        user_id: usersId[4],
        institution: 'Facebook',
    },
]);


