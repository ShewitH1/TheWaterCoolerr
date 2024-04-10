from repositories.db import get_pool
from psycopg.rows import dict_row
from datetime import datetime
import json

def get_job_posting_for_table(posting_id):
    if posting_id is None:
        return False
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
            poll.putconn(conn)