from repositories.db import get_pool
from psycopg.rows import dict_row
from datetime import datetime
import random

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
                                    firstname,
                                    profile_id
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

def get_user_profile_by_id(user_id):
    if user_id is None:
        return False
    pool = get_pool()
    try:
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute('''
                                SELECT
                                    profile_id,
                                    firstname,
                                    lastname,
                                    profile_image,
                                    profile_banner,
                                    profile_bio
                                FROM
                                    user_account
                                WHERE profile_id = %s
                                ''', [user_id])
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

#def get_company_profile_by_id(company_id):

# Creation Methods

def create_new_user_profile(profile_id, email, password, fname, lname):
    if profile_id is None or email is None or password is None or fname is None or lname is None:
        return None
    pool = get_pool()
    if check_user_id_taken(profile_id) or check_user_email_taken(email):
        return None
    try:
        profile_picture = get_random_default_profile()
        profile_banner = "img/site/default-profile/default-banner.png"
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute('''
                                INSERT INTO user_account(profile_id, email, pass, firstname, lastname, profile_image, profile_banner)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)
                                ''', (profile_id, email, password, fname, lname, profile_picture, profile_banner))
                conn.commit()
    except Exception as e:
        print(e)
        return None
    finally:
        if conn is not None:
            pool.putconn(conn)


# Helper Function for above method

def get_random_default_profile():
    banner_dict = {
        0 : "img/site/default-profile/default-profile-f-1.png",
        1 : "img/site/default-profile/default-profile-f-2.png",
        2 : "img/site/default-profile/default-profile-m-1.png",
        3 : "img/site/default-profile/default-profile-m-2.png"
    }
    rand = random.randint(0,3)
    return banner_dict[rand]

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

# Update Methods

def update_profile_bio(profile_type=None, profile_id=None, profile_bio=None):
    if profile_type is None or profile_id is None:
        return None
    pool = get_pool()
    try:
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                if (check_id_pair_exists(profile_type, profile_id, conn)):
                    if profile_type == 'user':
                        cursor.execute('''
                                        UPDATE
                                            user_account
                                        SET
                                            profile_bio = %s
                                        WHERE
                                            profile_id = %s
                                        ''', (profile_bio, profile_id))
                        conn.commit()
                    elif profile_type == 'company':
                        cursor.execute('''
                                        UPDATE
                                            company_account
                                        SET
                                            company_bio = %s
                                        WHERE
                                            company_id = %s
                                        ''', (profile_bio, profile_id))
                        conn.commit()
                    else:
                        return None
                else:
                    return None
    except Exception as e:
        print(e)
        return None
    finally:
        if conn is not None:
            pool.putconn(conn)

def update_profile_image(profile_type=None, profile_id=None, profile_picture=None):
    if profile_type is None or profile_id is None:
        return None
    pool = get_pool()
    try:
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                if (check_id_pair_exists(profile_type, profile_id, conn)):
                    if profile_type == 'user':
                        cursor.execute('''
                                        UPDATE
                                            user_account
                                        SET
                                            profile_image = %s
                                        WHERE
                                            profile_id = %s
                                        ''', (profile_picture, profile_id))
                        conn.commit()
                    elif profile_type == 'company':
                        cursor.execute('''
                                        UPDATE
                                            company_account
                                        SET
                                            company_image = %s
                                        WHERE
                                            company_id = %s
                                        ''', (profile_picture, profile_id))
                        conn.commit()
                    else:
                        return None
                else:
                    return None
    except Exception as e:
        print(e)
        return None
    finally:
        if conn is not None:
            pool.putconn(conn)

def update_profile_banner(profile_type=None, profile_id=None, profile_banner=None):
    if profile_type is None or profile_id is None:
        return None
    pool = get_pool()
    try:
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                if (check_id_pair_exists(profile_type, profile_id, conn)):
                    if profile_type == 'user':
                        cursor.execute('''
                                        UPDATE
                                            user_account
                                        SET
                                            profile_banner = %s
                                        WHERE
                                            profile_id = %s
                                        ''', (profile_banner, profile_id))
                        conn.commit()
                    elif profile_type == 'company':
                        cursor.execute('''
                                        UPDATE
                                            company_account
                                        SET
                                            company_banner = %s
                                        WHERE
                                            company_id = %s
                                        ''', (profile_banner, profile_id))
                        conn.commit()
                    else:
                        return None
                else:
                    return None
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

def check_id_pair_exists(profile_type=None, profile_id=None, conn=None):
    try:
        with conn.cursor(row_factory=dict_row) as cursor:
            if profile_type == 'user':
                cursor.execute('''
                                SELECT
                                    COUNT(*)
                                FROM
                                    user_account
                                WHERE profile_id = %s
                                ''', [profile_id])
                count = cursor.fetchone()['count']
                if count > 0:
                    return True
                else:
                    return False
            elif profile_type == 'company':
                cursor.execute('''
                                SELECT
                                    COUNT(*)
                                FROM
                                    company_account
                                WHERE company_id = %s
                                ''', [profile_id])
                count = cursor.fetchone()['count']
                if count > 0:
                    return True
                else:
                    return False
            else:
                return False
    except Exception as e:
        print(e)
        return False

