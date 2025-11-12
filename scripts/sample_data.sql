DELETE FROM review_app_book;

DELETE FROM auth_group;

DELETE FROM users_newuser;

DELETE FROM review_app_review;

INSERT INTO
    review_app_book (author, title)
VALUES
    (
        'J.K. Rowling',
        "Harry Potter and the Philosopher''s Stone"
    ),
    ('George Orwell', '1984'),
    ('J.R.R. Tolkien', 'The Fellowship of the Ring'),
    ('F. Scott Fitzgerald', 'The Great Gatsby'),
    ('Harper Lee', 'To Kill a Mockingbird'),
    ('Jane Austen', 'Pride and Prejudice'),
    ('Mark Twain', 'Adventures of Huckleberry Finn'),
    ('Ernest Hemingway', 'The Sun Also Rises'),
    ('Leo Tolstoy', 'War and Peace'),
    (
        'Gabriel García Márquez',
        'One Hundred Years of Solitude'
    ),
    ('Herman Melville', 'Moby Dick'),
    ('Victor Hugo', 'Les Misérables'),
    ('Mary Shelley', 'Frankenstein'),
    ('Charles Dickens', 'A Christmas Carol'),
    ('Aldous Huxley', 'Brave New World'),
    (
        'C.S. Lewis',
        'The Lion, the Witch and the Wardrobe'
    ),
    ('Homer', 'The Iliad'),
    ('Dante Alighieri', 'The Divine Comedy'),
    ('Franz Kafka', 'The Metamorphosis'),
    ('Miguel de Cervantes', 'Don Quixote');

INSERT INTO
    auth_group (name)
VALUES
    ("book_admin"),
    ("book_user");

INSERT INTO
    users_newuser (
        email,
        password,
        is_superuser,
        is_staff,
        is_active
    )
VALUES
    (
        'apultyn@example.com',
        'pbkdf2_sha256$1000000$Kf7ZxRtVdVcOhBMwXcNWG2$2ULZetIhYzBlcO4kDHXpm2j8aq7X4xHwLvXp0fNzl1w=',
        True,
        True,
        True
    ),
    (
        'mpultyn@example.com',
        'pbkdf2_sha256$1000000$Kf7ZxRtVdVcOhBMwXcNWG2$2ULZetIhYzBlcO4kDHXpm2j8aq7X4xHwLvXp0fNzl1w=',
        False,
        False,
        True
    ),
    (
        'bpultyn@example.com',
        'pbkdf2_sha256$1000000$Kf7ZxRtVdVcOhBMwXcNWG2$2ULZetIhYzBlcO4kDHXpm2j8aq7X4xHwLvXp0fNzl1w=',
        False,
        False,
        True
    );

INSERT INTO
    users_newuser_groups (newuser_id, group_id)
VALUES
    (3, 1),
    (1, 2),
    (2, 2),
    (3, 2);

INSERT INTO
    review_app_review (comment, stars, book_id, author_id)
VALUES
    (
        'A gripping narrative that kept me turning pages well past midnight.',
        5,
        1,
        1
    ),
    (
        'Solid world-building but the pacing drags in the middle.',
        3,
        1,
        2
    ),
    (
        'Unexpectedly moving—finished it in a single sitting.',
        5,
        2,
        2
    ),
    (
        'Enjoyable pulp adventure; perfect for a lazy weekend.',
        4,
        3,
        3
    ),
    (
        'Concept is intriguing, but characters felt flat.',
        2,
        4,
        1
    ),
    ('Masterful prose; every sentence sings.', 5, 5, 2),
    (
        'Not my cup of tea, but I can see why others rave.',
        3,
        6,
        3
    ),
    ('Quick read with a satisfying twist.', 4, 7, 2),
    (
        'Too predictable; I guessed the ending halfway through.',
        2,
        8,
        2
    ),
    (
        'Beautiful illustrations elevate a mediocre story.',
        3,
        9,
        1
    ),
    (
        'A dense but rewarding philosophical journey.',
        5,
        10,
        1
    ),
    ('Plot holes galore—left me frustrated.', 2, 11, 2),
    (
        'Heart-warming and funny in equal measure.',
        4,
        12,
        1
    ),
    (
        'Ambitious in scope, but fails to stick the landing.',
        3,
        13,
        3
    ),
    (
        'A chilling dystopia that feels all too possible.',
        5,
        14,
        1
    );