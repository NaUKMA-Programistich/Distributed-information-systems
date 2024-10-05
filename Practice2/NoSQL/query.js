// -- забрати рюзюме з іменем, прізвищем, телефоном та роком народження
db.resumes.aggregate([
    {
        $lookup: {
            from: 'users',
            localField: 'user_id',
            foreignField: '_id',
            as: 'user'
        }
    },
    { $unwind: '$user' },
    {
        $project: {
            _id: 1,
            title: 1,
            content: 1,
            first_name: '$user.profile.first_name',
            last_name: '$user.profile.last_name',
            phone: '$user.profile.phone',
            birth_year: '$user.profile.birth_year'
        }
    }
]);

// забрати всі резюме
db.resumes.find();

// забрати всі хоббі які існують в резюме
db.users.aggregate([
    {
        $match: {
            _id: { $in: db.resumes.distinct('user_id') }
        }
    },
    { $unwind: '$hobbies' },
    {
        $group: {
            _id: '$hobbies'
        }
    },
    {
        $lookup: {
            from: 'hobbies',
            localField: '_id',
            foreignField: '_id',
            as: 'hobby'
        }
    },
    { $unwind: '$hobby' },
    {
        $project: {
            _id: '$hobby._id',
            name: '$hobby.name'
        }
    }
]);

// забрати всі міста, що зустрічаються в резюме
db.users.aggregate([
    {
        $match: {
            _id: { $in: db.resumes.distinct('user_id') }
        }
    },
    {
        $group: {
            _id: '$profile.city'
        }
    },
    {
        $project: {
            city: '$_id',
            _id: 0
        }
    }
]);

// забрати хоббі всіх здобувачів, що мешкають в заданому місті
db.users.aggregate([
    {
        $match: {
            'profile.city': 'Kyiv'
        }
    },
    { $unwind: '$hobbies' },
    {
        $group: {
            _id: '$hobbies'
        }
    },
    {
        $lookup: {
            from: 'hobbies',
            localField: '_id',
            foreignField: '_id',
            as: 'hobby'
        }
    },
    { $unwind: '$hobby' },
    {
        $project: {
            name: '$hobby.name'
        }
    }
]);

// забрати всіх здобувачів, що працювали в одному закладі (заклад ми не вказуємо)
db.experiences.aggregate([
    {
        $group: {
            _id: "$institution",
            user_ids: { $addToSet: "$user_id" },
            count: { $sum: 1 }
        }
    },
    {
        $match: {
            count: { $gt: 1 }
        }
    },
    {
        $unwind: "$user_ids"
    },
    {
        $lookup: {
            from: "users",
            localField: "user_ids",
            foreignField: "_id",
            as: "user"
        }
    },
    {
        $unwind: "$user"
    },
    {
        $project: {
            institution: "$_id",
            first_name: "$user.profile.first_name",
            last_name: "$user.profile.last_name",
            _id: 0
        }
    }
]);
