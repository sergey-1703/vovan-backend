from passlib.context import CryptContext
import random
import string

pwd_context = CryptContext(schemes=["pbkdf2_sha256"])


def hash_password(password: str):
    return pwd_context.hash(password)



GROUPS = [
    ("alex", 35, "Alex group user"),
    ("anna", 35, "Anna group user"),
    ("test_user", 40, "Test account"),
    ("dev", 35, "Developer"),
    ("user", 40, "Regular user"),
    ("qa", 35, "QA engineer"),
]

NOISE_COUNT = 60



def random_login():
    prefixes = ["cool", "dark", "fast", "lazy", "smart", "crypto", "data", "bug", "coffee"]
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    return random.choice(prefixes) + "_" + suffix


def generate_users():
    users = []

    for prefix, count, about in GROUPS:
        for i in range(1, count + 1):
            login = f"{prefix}_{i}"
            nickname = prefix.capitalize() + str(i)

            password = f"{prefix}_{i}_pass"
            password_hash = hash_password(password)

            users.append((login, nickname, password_hash, about))

    for _ in range(NOISE_COUNT):
        login = random_login()
        nickname = login.capitalize()

        password_hash = hash_password("noise_pass")

        users.append((login, nickname, password_hash, "Random user"))

    return users


def generate_sql(users):
    lines = []

    lines.append("-- =====================================")
    lines.append("-- USERS SEED DATA")
    lines.append("-- =====================================")
    lines.append("""
-- ГРУППЫ:
-- alex_*        (~35)
-- anna_*        (~35)
-- test_user_*   (~40)
-- dev_*         (~35)
-- user_*        (~40)
-- qa_*          (~35)
-- + шум (~60)
--
-- Примеры тестов:
-- /search/alex/10/0
-- /search/test/20/20
-- /search/user/5/45
""")

    lines.append("INSERT INTO users (login, nickname, password_hash, about) VALUES")

    for i, (login, nickname, password_hash, about) in enumerate(users):
        line = f"('{login}', '{nickname}', '{password_hash}', '{about}')"

        if i < len(users) - 1:
            line += ","
        else:
            line += ";"

        lines.append(line)

    return "\n".join(lines)


if __name__ == "__main__":
    users = generate_users()
    random.shuffle(users)

    sql = generate_sql(users)

    with open("../sql_scripts/generate_test_users.sql", "w+", encoding="utf-8") as f:
        f.write(sql)

    print(f"✅ Сгенерировано пользователей: {len(users)}")
    print("📁 Файл: generate_test_users.sql")