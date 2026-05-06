import random
from datetime import datetime, timedelta

MAIN_USER_ID = 281

START_USER_ID = 2
END_USER_ID = 50

MIN_MESSAGES = 20
MAX_MESSAGES = 100

OUTPUT_FILE = "../../sql_scripts/generated_chats_messages.sql"

MESSAGES = [
    "Привет",
    "Как дела?",
    "Что делаешь?",
    "Ты тут?",
    "Окей",
    "Хорошо",
    "Понял",
    "Спасибо",
    "Да",
    "Нет",
    "Созвонимся позже",
    "Когда будешь свободен?",
    "Я уже отправил",
    "Посмотри сообщение",
    "Не забудь",
    "Это важно",
    "Хаха",
    "Интересно",
    "Я занят",
    "Перезвони",
    "Увидимся завтра",
    "Доброе утро",
    "Спокойной ночи",
]

chat_sql = []
message_sql = []

chat_id = 1
message_id = 1

current_time = datetime.now()

for other_user_id in range(START_USER_ID, END_USER_ID + 1):

    created_at = current_time.strftime("%Y-%m-%d %H:%M:%S")

    chat_sql.append(
        f"""INSERT INTO chats(id, user_main_id, user_chatter_id, created_at)
VALUES ({chat_id}, {MAIN_USER_ID}, {other_user_id}, '{created_at}');"""
    )

    messages_count = random.randint(MIN_MESSAGES, MAX_MESSAGES)

    message_time = current_time

    for _ in range(messages_count):

        sender_id = random.choice([MAIN_USER_ID, other_user_id])

        body = random.choice(MESSAGES).replace("'", "''")

        message_time += timedelta(
            minutes=random.randint(1, 60),
            seconds=random.randint(1, 59)
        )

        created_at = message_time.strftime("%Y-%m-%d %H:%M:%S")

        message_sql.append(
            f"""INSERT INTO messages(id, user_main_id, chat_id, body, created_at)
VALUES ({message_id}, {sender_id}, {chat_id}, '{body}', '{created_at}');"""
        )

        message_id += 1

    chat_id += 1

with open(OUTPUT_FILE, "w+", encoding="utf-8") as f:

    f.write("-- GENERATED CHATS\n\n")

    for line in chat_sql:
        f.write(line + "\n")

    f.write("\n\n-- GENERATED MESSAGES\n\n")

    for line in message_sql:
        f.write(line + "\n")

print(f"SQL file generated: {OUTPUT_FILE}")