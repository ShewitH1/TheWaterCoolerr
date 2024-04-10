from repositories.db import get_pool
from psycopg.rows import dict_row
from datetime import datetime
import json

def get_job_posting_by_id():
    pool = get_pool()
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
                            ''' 
                        )
            return cursor.fetchall()