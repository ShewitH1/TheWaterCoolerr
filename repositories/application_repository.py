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
            cur.execute("SELECT * FROM application_answers WHERE profile_id = %s AND posting_id = %s", (profile_id, posting_id))
            if cur.fetchone() is not None:
                return False
            set_application_status(posting_id, profile_id, 'waiting')
            for question_id, answer in answers.items():
                question_id = int(question_id)
                cur.execute("INSERT INTO application_answers (profile_id, posting_id, question_id, response_text) VALUES (%s, %s, %s, %s)", (profile_id, posting_id, question_id, answer))
        conn.commit()
    get_pool().putconn(conn)
    return True

def get_users_full_name(profile_id):
    if not profile_id:
        return None
    with get_pool().getconn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT firstname, lastname FROM user_account WHERE profile_id = %s", (profile_id,))
            user = cur.fetchone()
    get_pool().putconn(conn)
    return user

def get_applications_for_company(company_id):
    if not company_id:
        return None
    with get_pool().getconn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT DISTINCT ua.firstname, ua.lastname, jp.job_title, aa.posting_id, aa.profile_id 
                FROM user_account ua 
                INNER JOIN application_answers aa ON ua.profile_id = aa.profile_id 
                INNER JOIN job_posting jp ON aa.posting_id = jp.posting_id 
                LEFT JOIN user_application_data uad ON ua.profile_id = uad.profile_id AND aa.posting_id = uad.posting_id
                WHERE jp.company_id = %s AND (uad.application_status IS NULL OR uad.application_status NOT IN ('accepted', 'rejected'))
            """, (company_id,))
            applications = cur.fetchall()
    get_pool().putconn(conn)
    return applications

def get_user_answers_for_posting(profile_id, posting_id):
    if not profile_id or not posting_id:
        return None
    with get_pool().getconn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT question_id, response_text FROM application_answers WHERE profile_id = %s AND posting_id = %s", (profile_id, posting_id,))
            answers = cur.fetchall()
            print(answers)
    get_pool().putconn(conn)
    return answers

def set_application_status(posting_id, user_id, status):
    if not posting_id or not user_id or not status:
        return False
    with get_pool().getconn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM user_application_data WHERE posting_id = %s AND profile_id = %s", (posting_id, user_id))
            if cur.fetchone() is None:
                cur.execute("INSERT INTO user_application_data (profile_id, posting_id, application_status) VALUES (%s, %s, %s)", (user_id, posting_id, status))
            else:
                cur.execute("UPDATE user_application_data SET application_status = %s WHERE posting_id = %s AND profile_id = %s", (status, posting_id, user_id))
            conn.commit()
        get_pool().putconn(conn)
    return True

def get_applications_for_user(profile_id):
    if not profile_id:
        return None
    with get_pool().getconn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT DISTINCT jp.job_title, c.name, uad.application_status, aa.posting_id 
                FROM application_answers aa 
                INNER JOIN job_posting jp ON aa.posting_id = jp.posting_id 
                INNER JOIN company_account c ON jp.company_id = c.company_id 
                LEFT JOIN user_application_data uad ON aa.profile_id = uad.profile_id AND aa.posting_id = uad.posting_id
                WHERE aa.profile_id = %s
            """, (profile_id,))
            applications = cur.fetchall()
    get_pool().putconn(conn)
    return applications

def add_questions_to_posting(posting_id, questions):
    if not posting_id or not questions:
        print("Invalid input")
        return False
    with get_pool().getconn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM job_posting WHERE posting_id = %s", (posting_id,))
            if cur.fetchone() is None:
                print("Invalid posting_id")
                return False
            for question in questions:
                cur.execute("INSERT INTO application_questions (posting_id, question_text) VALUES (%s, %s)", (posting_id, question))
            conn.commit()
    return True