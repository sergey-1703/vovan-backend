CREATE TABLE IF NOT EXISTS users(
        id            SERIAL PRIMARY KEY,
        login         VARCHAR(255) NOT NULL,
        nickname      VARCHAR(255) NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        about         VARCHAR(255),
        is_banned BOOL DEFAULT False,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chats(
        id            SERIAL PRIMARY KEY,
        user_main_id INTEGER NOT NULL,
        user_chatter_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

CREATE TABLE IF NOT EXISTS messages(
        id            SERIAL PRIMARY KEY,
        user_main_id INTEGER NOT NULL,
        chat_id INTEGER NOT NULL,
        body VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );