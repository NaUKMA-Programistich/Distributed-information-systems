-- забрати рюзюме з іменем, прізвищем, телефоном та роком народження
SELECT resumes.*, profiles.first_name, profiles.last_name, profiles.phone, profiles.birth_year FROM resumes
    JOIN profiles ON resumes.user_id = profiles.user_id;

-- забрати всі резюме
SELECT * FROM resumes;

-- забрати всі хоббі які існують в резюме
SELECT DISTINCT hobby.id, hobby.name FROM hobbies hobby
    JOIN users_hobbies uh ON hobby.id = uh.hobby_id
    JOIN resumes resume ON uh.user_id = resume.user_id;

-- забрати всі міста, що зустрічаються в резюме
SELECT DISTINCT profile.user_id, profile.city FROM profiles profile
    JOIN resumes resume ON profile.user_id = resume.user_id;


-- забрати хоббі всіх здобувачів, що мешкають в заданому місті
SELECT DISTINCT hobby.id, hobby.name FROM hobbies hobby
    JOIN users_hobbies user_hobby ON hobby.id = user_hobby.hobby_id
    JOIN profiles profile ON user_hobby.user_id = profile.user_id
    JOIN resumes resume ON profile.user_id = resume.user_id
WHERE profile.city = 'Kyiv';

-- забрати всіх здобувачів, що працювали в одному закладі (заклад ми не вказуємо)
SELECT DISTINCT profile.user_id, profile.first_name, profile.last_name, experience.institution FROM profiles profile
    JOIN experiences experience ON profile.user_id = experience.user_id
WHERE experience.institution IN (
    SELECT institution
    FROM experiences
    GROUP BY institution
    HAVING COUNT(DISTINCT user_id) > 1
);
