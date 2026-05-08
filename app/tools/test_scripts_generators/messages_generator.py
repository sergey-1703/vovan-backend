import random
from datetime import datetime, timedelta

MAIN_USER_ID = 281

DIALOG_START_ID = 2
DIALOG_END_ID = 20

ALL_USERS_START = 1
ALL_USERS_END = 30

SIDE_CHATS_COUNT = 15

MIN_MESSAGES = 5
MAX_MESSAGES = 25

OUTPUT_FILE = "../../sql_scripts/generated_chats_messages.sql"

MESSAGES = [
    "Привет",
    "Как дела?",
    "Ты тут?",
    "Что делаешь?",
    "Доброе утро",
    "Спокойной ночи",
    "Я занят",
    "Созвонимся позже",
    "Отправил файл",
    "Посмотри сообщение",
    "Не забудь",
    "Когда встречаемся?",
    "Хорошо",
    "Окей",
    "Да",
    "Нет",
    "Понял",
    "Спасибо",
    "Увидимся завтра",
    "Работаю",
    "Почти готово",
    "Сейчас сделаю",
    "Жду ответ",
    "Интересно",
    "Хаха",
]

chat_sql = []
message_sql = []

chat_id = 1
message_id = 1

used_chats = set()

for other_user in range(DIALOG_START_ID, DIALOG_END_ID + 1):

    if random.choice([True, False]):
        user_main = MAIN_USER_ID
        user_chatter = other_user
    else:
        user_main = other_user
        user_chatter = MAIN_USER_ID

    used_chats.add(tuple(sorted((MAIN_USER_ID, other_user))))

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    chat_sql.append(
        f"""INSERT INTO chats(id, user_main_id, user_chatter_id, created_at)
VALUES ({chat_id}, {user_main}, {user_chatter}, '{created_at}');"""
    )

    messages_count = random.randint(MIN_MESSAGES, MAX_MESSAGES)

    current_time = datetime.now()

    for _ in range(messages_count):

        sender = random.choice([MAIN_USER_ID, other_user])

        body = random.choice(MESSAGES).replace("'", "''")

        current_time += timedelta(
            minutes=random.randint(1, 120)
        )

        created_at = current_time.strftime("%Y-%m-%d %H:%M:%S")

        message_sql.append(
            f"""INSERT INTO messages(id, user_main_id, chat_id, body, created_at)
VALUES ({message_id}, {sender}, {chat_id}, '{body}', '{created_at}');"""
        )

        message_id += 1

    chat_id += 1

while SIDE_CHATS_COUNT > 0:

    user1 = random.randint(ALL_USERS_START, ALL_USERS_END)
    user2 = random.randint(ALL_USERS_START, ALL_USERS_END)

    if user1 == user2:
        continue

    pair = tuple(sorted((user1, user2)))

    if pair in used_chats:
        continue

    used_chats.add(pair)

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    chat_sql.append(
        f"""INSERT INTO chats(id, user_main_id, user_chatter_id, created_at)
VALUES ({chat_id}, {user1}, {user2}, '{created_at}');"""
    )

    messages_count = random.randint(MIN_MESSAGES, MAX_MESSAGES)

    current_time = datetime.now()

    for _ in range(messages_count):

        sender = random.choice([user1, user2])

        body = random.choice(MESSAGES).replace("'", "''")

        current_time += timedelta(
            minutes=random.randint(1, 120)
        )

        created_at = current_time.strftime("%Y-%m-%d %H:%M:%S")

        message_sql.append(
            f"""INSERT INTO messages(id, user_main_id, chat_id, body, created_at)
VALUES ({message_id}, {sender}, {chat_id}, '{body}', '{created_at}');"""
        )

        message_id += 1

    chat_id += 1
    SIDE_CHATS_COUNT -= 1

with open(OUTPUT_FILE, "w+", encoding="utf-8") as f:

    for line in chat_sql:
        f.write(line + "\n")

    f.write("\n\n")

    for line in message_sql:
        f.write(line + "\n")

print(f"Generated: {OUTPUT_FILE}")