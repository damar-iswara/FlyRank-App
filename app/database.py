import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg.connect(DATABASE_URL)


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    done BOOLEAN NOT NULL DEFAULT FALSE
                )
            """)

            cursor.execute("SELECT COUNT(*) FROM tasks")
            count = cursor.fetchone()[0]

            if count == 0:
                example_tasks = [
                    ("Learn FastAPI", False),
                    ("Build a REST API", False),
                    ("Practice API testing", True),
                ]

                cursor.executemany(
                    "INSERT INTO tasks (title, done) VALUES (%s, %s)",
                    example_tasks
                )

        conn.commit()


# ------------ Helper functions ------------
def check_id_exists(id: int):
    # Check if the task with the given ID exists in the database
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM tasks WHERE id = %s LIMIT 1", (id,))
            exists = cursor.fetchone() is not None

    return exists


def check_title_not_empty(title: str):
    # Check if the title is not empty
    return bool(title.strip())