import psycopg
from repositories.db import get_pool

def get_questions_for_application(posting_id):
    with get_pool().getconn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM application_questions WHERE posting_id = %s", (posting_id,))
            questions = cur.fetchall()
    get_pool().putconn(conn)
    return questions

def submit_application(profile_id, posting_id, answers):
    if not profile_id:
        return False
    with get_pool().getconn() as conn:
        with conn.cursor() as cur:
            for question_id, answer in answers.items():
                cur.execute("INSERT INTO application_answers (profile_id, posting_id, question_id, response_text) VALUES (%s, %s, %s, %s)", (profile_id, posting_id, question_id, answer))
        conn.commit()
    get_pool().putconn(conn)
    return True