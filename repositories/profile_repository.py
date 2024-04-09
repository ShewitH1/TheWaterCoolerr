from repositories.db import get_pool
from psycopg.rows import dict_row
from datetime import datetime
import json

# User Profile Get Methods

def get_user_by_login(login):
    if login is None:
        return False
    pool = get_pool()
    try:
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute('''
                                SELECT
                                    email,
                                    pass AS hashed_password,
                                    firstname
                                FROM
                                    user_account
                                WHERE email = %s
                                ''', [login])
                return cursor.fetchone()
    except Exception as e:
        print(e)
        return False
    finally:
        if conn is not None:
            pool.putconn(conn)

# Company Profile Get Methods

def get_company_by_login(company_login):
    if company_login is None:
        return False
    pool = get_pool()
    try:
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute('''
                                SELECT
                                    login,
                                    pass AS hashed_password
                                FROM
                                    company_account
                                WHERE login = %s
                                ''', [company_login])
                return cursor.fetchone()
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
def create_new_company_profile(company_id, company_login, password, company_name):
    if company_id is None or company_login is None or password is None or company_name is None:
        return None
    pool = get_pool()
    if check_company_id_taken(company_id):
        return None
    try:
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute('''
                                INSERT INTO company_account(company_id, login, pass, name)
                                VALUES (%s, %s, %s, %s)
                                ''', (company_id, company_login, password, company_name))
                conn.commit()
    except Exception as e:
        print(e)
        return None
    finally:
        if conn is not None:
            pool.putconn(conn)

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

def check_company_id_taken(new_id):
    if new_id is None:
        return None
    pool = get_pool()
    try:
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute('''
                                SELECT
                                    company_id
                                FROM
                                    company_account
                                WHERE company_id = %s
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
