set_one = {
    "users":
    (
        "id SERIAL UNIQUE",
        "first_name VARCHAR(255)",
        "last_name VARCHAR(255)",
        "email TEXT UNIQUE"
    ),
    "posts": (
        "id SERIAL UNIQUE",
        "content TEXT",
        "user_id INT UNIQUE NOT NULL",
        "CONSTRAINT user_fk FOREIGN KEY(user_id) REFERENCES users(id)"
    )
}