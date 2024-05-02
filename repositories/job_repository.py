from repositories.db import get_pool
from psycopg.rows import dict_row
from datetime import datetime
import uuid

def indi_job_posting(job_id):
    conn = None
    pool = get_pool()
    try:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(''' 
                                SELECT 
                                        j.job_title,
                                        j.posting_id,
                                        c.company_id,
                                        j.location,
                                        j.company,
                                        j.posting_date,
                                        j.salary,
                                        j.job_description,
                                        responsibilities,
                                        requirements
                                FROM 
                                        job_posting j
                                JOIN company_account c on j.company_id = c.company_id 
                                WHERE j.posting_id = %s
                                ;
                                ''', (job_id,))
                return cursor.fetchone()
    except Exception as e:
        print(e)
        return False

def get_job_postings():
    conn = None
    pool = get_pool()
    try:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute('''
                        SELECT
                                j.job_title,
                                j.posting_date,
                                j.description,
                                j.salary,
                                j.location,
                                j.company,
                                c.company_id,
                                j.posting_id
                        FROM 
                                job_posting j
                        Join company_account c on j.company_id = c.company_id 
                                ;''') 
                return cursor.fetchall()
    except Exception as e:
        print(e)
        return False

def get_job_posting_for_table(posting_id):
    if posting_id is None:
        return False
    conn = None
    pool = get_pool()
    try:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute('''
                        SELECT
                                j.job_title,
                                j.posting_date,
                                j.description,
                                j.salary,
                                c.company_id
                        FROM 
                                job_posting j
                        Join company_account c on j.company_id = c.company_id 
                        WHERE j.posting_id = %s
                            ;
                                ''', [posting_id]) 
                return cursor.fetchone()
    except Exception as e:
        print(e)
        return False
    finally:
        if conn is not None:
            pool.putconn(conn)

def create_job_posting(job_title, posting_date, description, salary, company_id):
    pool = get_pool()
    posting_id = str(uuid.uuid4()).replace('-', '')[:24]
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('''
                        INSERT INTO job_posting (posting_id, job_title, posting_date, description, salary, company_id)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        RETURNING posting_id;
                                ''', [posting_id, job_title, posting_date, description, salary, company_id]) 
                return posting_id
    except Exception as e:
        print(e)
        return None

def update_job_posting(posting_id, job_title, posting_date, description, salary, company_id):
    conn = None
    pool = get_pool()
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('''
                        UPDATE job_posting
                        SET job_title = %s, posting_date = %s, description = %s, salary = %s, company_id = %s
                        WHERE posting_id = %s
                                ''', [job_title, posting_date, description, salary, company_id, posting_id]) 
                return True
    except Exception as e:
        print(e)
        return False
    finally:
        if conn is not None:
            pool.putconn(conn)
            
def search_jobs(job_title, location, company):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                            SELECT 
                                posting_id,
                                job_title,
                                salary,
                                company, 
                                location,
                                description,
                                company_id,
                                posting_date
                            FROM 
                                job_posting
                            WHERE 
                                job_title ILIKE %s
                                AND location ILIKE %s
                                AND company ILIKE %s
                        ''', ('%' + job_title + '%', '%' + location + '%', '%' + company + '%'))
            return cursor.fetchall()

def delete_job_posting(posting_id):
    conn = None
    pool = get_pool()
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('''
                            DELETE FROM job_posting
                            WHERE posting_id = %s
                                    ;
                            ''', [posting_id]) 
                return True
    except Exception as e:
        print(e)
        return False
    finally:
        if conn is not None:
            pool.putconn(conn)

