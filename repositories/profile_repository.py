from repositories.db import get_pool
from psycopg.rows import dict_row
from datetime import datetime
import random

# User Profile Get Methods

def get_user_by_login(login):
    if login is None:
        return None
    conn = None
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
        return None
    finally:
        if conn is not None:
            pool.putconn(conn)

def get_user_profile_by_id(user_id):
    if user_id is None:
        return None
    conn = None
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
        return None
    finally:
        if conn is not None:
            pool.putconn(conn)

# Company Profile Get Methods

def get_company_by_login(company_login):
    if company_login is None:
        return None
    conn = None
    pool = get_pool()
    try:
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute('''
                                SELECT
                                    company_id,
                                    login,
                                    pass AS hashed_password
                                FROM
                                    company_account
                                WHERE login = %s
                                ''', [company_login])
                return cursor.fetchone()
    except Exception as e:
        print(e)
        return None
    finally:
        if conn is not None:
            pool.putconn(conn)

def get_company_profile_by_id(company_id):
    if company_id is None:
        return None
    conn = None
    pool = get_pool()
    try:
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute('''
                                SELECT
                                    company_id,
                                    company_image,
                                    company_banner,
                                    company_bio,
                                    about_img_1,
                                    about_img_2,
                                    about_img_3,
                                    name
                                FROM
                                    company_account
                                WHERE company_id = %s
                                ''', [company_id])
                return cursor.fetchone()
    except Exception as e:
        print(e)
        return None
    finally:
        if conn is not None:
            pool.putconn(conn)

# Creation Methods

def create_new_user_profile(profile_id, email, password, fname, lname):
    if profile_id is None or email is None or password is None or fname is None or lname is None:
        return None
    conn = None
    pool = get_pool()
    if check_id_taken(profile_id) or check_user_email_taken(email):
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
    profile_dict = {
        0 : "img/site/default-profile/default-profile-f-1.png",
        1 : "img/site/default-profile/default-profile-f-2.png",
        2 : "img/site/default-profile/default-profile-m-1.png",
        3 : "img/site/default-profile/default-profile-m-2.png"
    }
    rand = random.randint(0,3)
    return profile_dict[rand]

def get_random_default_profile_company():
    profile_dict = {
        0 : "img/site/default-profile/default-profile-company-1.png",
        1 : "img/site/default-profile/default-profile-company-2.png",
        2 : "img/site/default-profile/default-profile-company-3.png",
        3 : "img/site/default-profile/default-profile-company-4.png"
    }
    rand = random.randint(0,3)
    return profile_dict[rand]

def get_random_default_banner_company():
    banner_dict = {
        0 : "img/site/default-profile/default-banner-company-1.png",
        1 : "img/site/default-profile/default-banner-company-2.png"
    }
    rand = random.randint(0,1)
    return banner_dict[rand]

#def create_new_company_profile(company_id, login, password, cname):

def create_new_company_profile(company_id, company_login, password, company_name):
    if company_id is None or company_login is None or password is None or company_name is None:
        return None
    conn = None
    pool = get_pool()
    if check_id_taken(company_id):
        return None
    try:
        profile_picture = get_random_default_profile_company()
        profile_banner = get_random_default_banner_company()
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute('''
                                INSERT INTO company_account(company_id, login, pass, name, company_image, company_banner)
                                VALUES (%s, %s, %s, %s, %s, %s)
                                ''', (company_id, company_login, password, company_name, profile_picture, profile_banner))
                conn.commit()
    except Exception as e:
        print(e)
        return None
    finally:
        if conn is not None:
            pool.putconn(conn)

# Update Methods

def update_profile_firstname(profile_id=None, firstname=None):
    if profile_id is None or firstname is None:
        return None
    conn = None
    pool = get_pool()
    try:
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                if (check_id_pair_exists("user", profile_id, conn)):
                    cursor.execute('''
                                        UPDATE
                                            user_account
                                        SET
                                            firstname = %s
                                        WHERE
                                            profile_id = %s
                                        ''', (firstname, profile_id))
                    conn.commit()
                else:
                    return None
    except Exception as e:
        print(e)
        return None
    finally:
        if conn is not None:
            pool.putconn(conn)

def update_profile_lastname(profile_id=None, lastname=None):
    if profile_id is None or lastname is None:
        return None
    conn = None
    pool = get_pool()
    try:
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                if (check_id_pair_exists("user", profile_id, conn)):
                    cursor.execute('''
                                        UPDATE
                                            user_account
                                        SET
                                            lastname = %s
                                        WHERE
                                            profile_id = %s
                                        ''', (lastname, profile_id))
                    conn.commit()
                else:
                    return None
    except Exception as e:
        print(e)
        return None
    finally:
        if conn is not None:
            pool.putconn(conn)

def update_company_name(profile_id=None, name=None):
    if profile_id is None:
        return -4
    if name is None:
        return -3
    conn = None
    pool = get_pool()
    try:
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                if (check_id_pair_exists("company", profile_id, conn)):
                    cursor.execute('''
                                        UPDATE
                                            company_account
                                        SET
                                            name = %s
                                        WHERE
                                            company_id = %s
                                        ''', (name, profile_id))
                    conn.commit()
                    return 0
                else:
                    return -2
    except Exception as e:
        print(e)
        return -1
    finally:
        if conn is not None:
            pool.putconn(conn)

def update_profile_bio(profile_type=None, profile_id=None, profile_bio=None):
    if profile_id is None:
        return -4
    if profile_type is None:
        return -3
    if profile_bio is None:
        return -2
    conn = None
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
                        return 0
                    else:
                        return -5
                else:
                    return -6
    except Exception as e:
        print(e)
        return -1
    finally:
        if conn is not None:
            pool.putconn(conn)

def update_profile_image(profile_type=None, profile_id=None, profile_picture=None):
    if profile_type is None or profile_id is None:
        return None
    conn = None
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
    conn = None
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

def update_about_img(profile_id=None, about_img=None, id=0):
    if profile_id is None:
        return -4
    if about_img is None:
        return -3
    if id > 3 or id < 0:
        return -2
    conn = None
    pool = get_pool()
    try:
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                if id == 0:
                    cursor.execute('''
                                    UPDATE
                                        company_account
                                    SET
                                        about_img_1 = %s
                                    WHERE
                                        company_id = %s
                                    ''', (about_img, profile_id))
                    conn.commit()
                elif id == 1:
                    cursor.execute('''
                                    UPDATE
                                        company_account
                                    SET
                                        about_img_2 = %s
                                    WHERE
                                        company_id = %s
                                    ''', (about_img, profile_id))
                    conn.commit()
                elif id == 2:
                    cursor.execute('''
                                    UPDATE
                                        company_account
                                    SET
                                        about_img_3 = %s
                                    WHERE
                                        company_id = %s
                                    ''', (about_img, profile_id))
                    conn.commit()
    except Exception as e:
        print("Failure updating about image")
        print(e)
    finally:
        if conn is not None:
            pool.putconn(conn)

            
# Logic Methods

def check_id_taken(new_id):
    if new_id is None:
        return None
    conn = None
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
                cursor.execute('''
                                SELECT
                                    company_id
                                FROM
                                    company_account
                                WHERE company_id = %s
                                ''', [new_id])
                company_id = cursor.fetchone()
                if company_id is None:
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
    conn = None
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

# def check_company_id_taken(new_id):
#     if new_id is None:
#         return None
#     conn = None
#     pool = get_pool()
#     try:
#         with pool.getconn() as conn:
#             with conn.cursor(row_factory=dict_row) as cursor:
#                 cursor.execute('''
#                                 SELECT
#                                     company_id
#                                 FROM
#                                     company_account
#                                 WHERE company_id = %s
#                                 ''', [new_id])
#                 profile_id = cursor.fetchone()
#                 if profile_id is None:
#                     return False
#                 return True
#     except Exception as e:
#         print(e)
#         return None
#     finally:
#         if conn is not None:
#             pool.putconn(conn)

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

# Workplace Experience Methods

def create_new_workplace_experience(profile_id):
    if profile_id is None:
        return None
    conn = None
    pool = get_pool()
    try:
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute('''
                                INSERT INTO workplace_experience(profile_id)
                                VALUES (%s)
                                RETURNING work_experience_id
                                ''', [profile_id])
                inserted_uuid = cursor.fetchone()['work_experience_id']
                conn.commit()
                return inserted_uuid
    except Exception as e:
        print("error creating new workplace experience")
        print(e)
        return None
    finally:
        if (conn is not None):
            pool.putconn(conn)

def update_work_experience_by_id(exp_id, title, cmpy_name, sector, start_date, end_date, description, water_cooler):
    if exp_id is None:
        return -2
    if title is None or cmpy_name is None:
        return -1
    conn = None
    pool = get_pool()
    try:
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute('''
                                UPDATE 
                                    workplace_experience
                                SET
                                    job_title = %s,
                                    company_name = %s,
                                    job_sector = %s,
                                    start_date = %s,
                                    end_date = %s,
                                    description = %s,
                                    watercooler = %s
                                WHERE
                                    work_experience_id = %s
                                ''', (title, cmpy_name, sector, start_date, end_date, description, water_cooler, exp_id))
                conn.commit()
                return 1
    except Exception as e:
        print("Failed to update workplace experience with id ", exp_id)
        print(e)
        return -3
    finally:
        if (conn is not None):
            pool.putconn(conn)


def get_all_workplace_experience_by_profile(profile_id):
    if profile_id is None:
        return None
    conn = None
    pool = get_pool()
    try:
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute('''
                                SELECT
                                    work_experience_id,
                                    job_title,
                                    company_name,
                                    job_sector,
                                    start_date,
                                    end_date,
                                    description,
                                    watercooler
                                FROM
                                    workplace_experience
                                WHERE profile_id = %s
                                ''', [profile_id])
                return cursor.fetchall()
    except Exception as e:
        print(e)
        return None
    finally:
        if (conn is not None):
            pool.putconn(conn)

def delete_work_experience_by_id(exp_id):
    if exp_id is None:
        return -1
    conn = None
    pool = get_pool()
    try:
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute('''
                                DELETE 
                                FROM 
                                    workplace_experience
                                WHERE work_experience_id = %s
                                ''', [exp_id])
                conn.commit()
                return 1
    except Exception as e:
        print(e)
        return None
    finally:
        if (conn is not None):
            pool.putconn(conn)

# Education Experience Methods

def create_new_education_experience(profile_id):
    if profile_id is None:
        return None
    conn = None
    pool = get_pool()
    try:
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute('''
                                INSERT INTO education_experience(profile_id)
                                VALUES (%s)
                                RETURNING education_experience_id
                                ''', [profile_id])
                inserted_uuid = cursor.fetchone()['education_experience_id']
                conn.commit()
                return inserted_uuid
    except Exception as e:
        print("error creating new education experience")
        print(e)
        return None
    finally:
        if (conn is not None):
            pool.putconn(conn)

def update_education_experience_by_id(exp_id, inst_name, edu_level, stu_area, start_date, end_date):
    if exp_id is None:
        return -5
    if inst_name is None:
        return -4
    if edu_level is None: 
        return -3
    if start_date is None:
        return -2
    conn = None
    pool = get_pool()
    try:
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute('''
                                UPDATE 
                                    education_experience
                                SET
                                    institution_name = %s,
                                    education_level = %s,
                                    study_area = %s,
                                    start_date = %s,
                                    end_date = %s
                                WHERE
                                    education_experience_id = %s
                                ''', (inst_name, edu_level, stu_area, start_date, end_date, exp_id))
                conn.commit()
                return 1
    except Exception as e:
        print("Failed to update workplace experience with id ", exp_id)
        print(e)
        return -1
    finally:
        if (conn is not None):
            pool.putconn(conn)


def get_all_education_experience_by_profile(profile_id):
    if profile_id is None:
        return None
    conn = None
    pool = get_pool()
    try:
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute('''
                                SELECT
                                    education_experience_id,
                                    profile_id,
                                    institution_name,
                                    education_level,
                                    study_area,
                                    start_date,
                                    end_date
                                FROM
                                    education_experience
                                WHERE profile_id = %s
                                ''', [profile_id])
                return cursor.fetchall()
    except Exception as e:
        print(e)
        return None
    finally:
        if (conn is not None):
            pool.putconn(conn)

def delete_education_experience_by_id(exp_id):
    if exp_id is None:
        return -1
    conn = None
    pool = get_pool()
    try:
        with pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute('''
                                DELETE 
                                FROM 
                                    education_experience
                                WHERE education_experience_id = %s
                                ''', [exp_id])
                conn.commit()
                return 1
    except Exception as e:
        print(e)
        return None
    finally:
        if (conn is not None):
            pool.putconn(conn)