from repositories.db import get_pool
from psycopg.rows import dict_row
from datetime import datetime
import uuid

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
                                c.company_id
                        FROM 
                                job_posting j
                        Join company_account c on j.company_id = c.company_id 
                                ;''') 
                return cursor.fetchall()
    except Exception as e:
        print(e)
        return False
    finally:
        if conn is not None:
            conn.close()  # Close the connection instead of returning it to the pool

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

def search_job_posting(job_title, posting_date, description, salary, company_id):
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
                        WHERE 
                                j.job_title = %s AND
                                j.posting_date = %s AND
                                j.description = %s AND
                                j.salary = %s AND
                                j.company_id = %s
                            ;
                                ''', [job_title, posting_date, description, salary, company_id]) 
                return cursor.fetchall()
    except Exception as e:
        print(e)
        return False
    finally:
        if conn is not None:
            pool.putconn(conn)

def delete_job_posting(posting_id):
    conn = None
    pool = get_pool()
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('''
                        DELETE FROM job_posting
                        WHERE posting_id = %s
                                ''', [posting_id]) 
                return True
    except Exception as e:
        print(e)
        return False
    finally:
        if conn is not None:
            pool.putconn(conn)

