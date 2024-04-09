from repositories.db import get_pool
from psycopg.rows import dict_row
from datetime import datetime
import json

# User Profile Get Methods

def get_user_by_id(user_id):
    if user_id is None:
        return False
    pool = get_pool()
    try:
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute('''
                                SELECT
                                    *
                                FROM
                                    user_account
                                WHERE profile_id = %s
                                ''', [user_id])
                return cursor.fetchall()
    except Exception as e:
        print(e)
        return False
    finally:
        if conn is not None:
            pool.putconn(conn)

# Company Profile Get Methods

def get_company_by_id(company_id):
    if company_id is None:
        return False
    pool = get_pool()
    try:
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute('''
                                SELECT
                                    *
                                FROM
                                    company_account
                                WHERE company_id = %s
                                ''', [company_id])
                return cursor.fetchall()
    except Exception as e:
        print(e)
        return False
    finally:
        if conn is not None:
            pool.putconn(conn)

# Creation Methods

def create_new_user_profile(profile_id, email, password, fname, lname):
    if profile_id is None or email is None or password is None or fname is None or lname is None:
        return None
    pool = get_pool()
    if check_user_id_taken(profile_id) or check_user_email_taken(email):
        return None
    try:
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute('''
                                INSERT INTO user_account(profile_id, email, pass, firstname, lastname)
                                VALUES (%s, %s, %s, %s, %s)
                                ''', (profile_id, email, password, fname, lname))
                conn.commit()
    except Exception as e:
        print(e)
        return None
    finally:
        if conn is not None:
            pool.putconn(conn)


#def create_new_company_profile(company_id, login, password, cname):

# Logic Methods

def check_user_id_taken(new_id):
    if new_id is None:
        return None
    pool = get_pool()
    try:
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute('''
                                SELECT
                                    profile_id
                                FROM
                                    user_account
                                WHERE profile_id = %s
                                ''', [new_id])
                profile_id = cursor.fetchone()
                if profile_id is None:
                    return False
                return True
    except Exception as e:
        print(e)
        return None
    finally:
        if conn is not None:
            pool.putconn(conn)

def check_user_email_taken(new_email):
    if new_email is None:
        return None
    pool = get_pool()
    try:
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute('''
                                SELECT
                                    email
                                FROM
                                    user_account
                                WHERE email = %s
                                ''', [new_email])
                email = cursor.fetchone()
                if email is None:
                    return False
                return True
    except Exception as e:
        print(e)
        return None
    finally:
        if conn is not None:
            pool.putconn(conn)