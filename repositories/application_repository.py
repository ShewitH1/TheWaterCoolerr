import psycopg
from repositories.db import get_pool

def get_questions_for_application(posting_id):
    with get_pool().getconn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM application_questions WHERE posting_id = %s", (posting_id,))
            questions = cur.fetchall()
    get_pool().putconn(conn)
    return questions