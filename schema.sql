CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS user_account (
    profile_id VARCHAR(16) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    pass VARCHAR(255) NOT NULL,
    firstname VARCHAR(64) NOT NULL,
    lastname VARCHAR(64) NOT NULL,
    profile_image VARCHAR(255),
    profile_banner VARCHAR(255),
    profile_bio VARCHAR(128),
    is_auth BOOLEAN,
    PRIMARY KEY (profile_id)
);

CREATE TABLE IF NOT EXISTS company_account (
    company_id VARCHAR(16) UNIQUE NOT NULL,
    login VARCHAR(255) UNIQUE NOT NULL,
    pass VARCHAR(255) NOT NULL,
    name VARCHAR(64) UNIQUE NOT NULL,
    company_image VARCHAR(255),
    company_banner VARCHAR(255),
    about_img_1 VARCHAR(255),
    about_img_2 VARCHAR(255),
    about_img_3 VARCHAR(255),
    company_bio TEXT,
    is_auth BOOLEAN,
    PRIMARY KEY (company_id)
);

CREATE TABLE IF NOT EXISTS workplace_experience (
    work_experience_id UUID DEFAULT uuid_generate_v4 (),
    profile_id VARCHAR(16) NOT NULL,
    job_title VARCHAR(64),
    company_name VARCHAR(64),
    job_sector VARCHAR(64),
    start_date VARCHAR(10),
    end_date VARCHAR(10),
    description TEXT,
    watercooler BOOLEAN,
    PRIMARY KEY (work_experience_id),
    FOREIGN KEY (profile_id) REFERENCES user_account(profile_id) ON UPDATE CASCADE ON DELETE CASCADE
);

DROP TYPE IF EXISTS education_level;
CREATE TYPE education_level AS ENUM('GED', 'Certification', 'Bachelors', 'Masters', 'PhD');

CREATE TABLE IF NOT EXISTS education_experience (
    education_experience_id UUID DEFAULT uuid_generate_v4 (),
    profile_id VARCHAR(16),
    institution_name VARCHAR(128),
    education_level VARCHAR(32),
    study_area VARCHAR(64),
    start_date VARCHAR(10),
    end_date VARCHAR(10),
    PRIMARY KEY (education_experience_id),
    FOREIGN KEY (profile_id) REFERENCES user_account(profile_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS job_posting (
    posting_id VARCHAR(24),
    company_id VARCHAR(16) NOT NULL,
    job_title VARCHAR(64) NOT NULL,
    description TEXT NOT NULL,
    salary FLOAT NOT NULL,
    posting_date timestamp DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (posting_id),
    FOREIGN KEY (company_id) REFERENCES company_account(company_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS posting_tags (
    
);

CREATE TABLE application_questions (
    id SERIAL PRIMARY KEY,
    posting_id VARCHAR(24),
    question_text TEXT NOT NULL,
    response_text TEXT,
    FOREIGN KEY (posting_id) REFERENCES job_posting(posting_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE application_answers (
    id SERIAL PRIMARY KEY,
    profile_id VARCHAR(16) NOT NULL,
    posting_id VARCHAR(24) NOT NULL,
    question_id INTEGER NOT NULL,
    response_text TEXT NOT NULL,
    FOREIGN KEY (profile_id) REFERENCES user_account(profile_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (posting_id) REFERENCES job_posting(posting_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES application_questions(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE user_application_data (
    id SERIAL PRIMARY KEY,
    profile_id VARCHAR(16) NOT NULL,
    posting_id VARCHAR(24) NOT NULL,
    application_status VARCHAR(32) NOT NULL,
    FOREIGN KEY (profile_id) REFERENCES user_account(profile_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (posting_id) REFERENCES job_posting(posting_id) ON UPDATE CASCADE ON DELETE CASCADE
);

INSERT INTO company_account (company_id, login, pass, name, company_image, company_banner, company_bio, is_auth)
VALUES ('COMP001', 'comp', 'abc', 'theman', 'image', 'image', 'this is a real comp', true);

INSERT INTO company_account (company_id, login, pass, name, company_image, company_banner, company_bio, is_auth)
VALUES ('COMP002', 'joke', '123', 'Prolific Portrayol', 'clown', 'improv', 'Improv group who never says no ;)', true);

INSERT INTO company_account (company_id, login, pass, name, company_image, company_banner, company_bio, is_auth)
VALUES ('COMP003', 'hire', 'xyz', 'Boston Consoling Group', 'group_hug', 'therapy office', 'Not to be confused with the consulting company', true);

INSERT INTO company_account (company_id, login, pass, name, company_image, company_banner, company_bio, is_auth)
VALUES ('COMP004', 'live', 'wire', 'School of Hard Rock', 'concert', 'guitar hero 3', 'We are here to rock!', true);

INSERT INTO user_account (profile_id, email, pass, firstname, lastname, profile_image, profile_banner, profile_bio, is_auth)
VALUES ('USER001', 'johnsmith@gmail.com', 'password', 'John', 'Smith', 'profile_image', 'profile_banner', 'I am a software engineer with a passion for technology.', true);

INSERT INTO job_posting (posting_id, company_id, job_title, description, salary)
VALUES ('POST001', 'COMP001', 'Software Engineer', 'We are seeking a highly skilled software engineer to join our dynamic team.', 80000.00);

INSERT INTO job_posting (posting_id, company_id, job_title, description, salary)
VALUES ('POST002', 'COMP002', 'Data Analyst', 'We are looking for a talented data analyst to help us analyze and interpret data.', 60000.00);

INSERT INTO job_posting (posting_id, company_id, job_title, description, salary)
VALUES ('POST003', 'COMP003', 'Marketing Manager', 'Join our marketing team and lead strategic marketing initiatives.', 70000.00);

INSERT INTO job_posting (posting_id, company_id, job_title, description, salary)
VALUES ('POST004', 'COMP004', 'Graphic Designer', 'Create stunning visuals and designs for our marketing campaigns.', 55000.00);

INSERT INTO job_posting (posting_id, company_id, job_title, description, salary)
VALUES ('POST005', 'COMP002', 'Business Development Manager', 'Drive business growth through strategic partnerships and initiatives.', 75000.00);

INSERT INTO job_posting (posting_id, company_id, job_title, description, salary)
VALUES ('POST006', 'COMP001', 'Product Manager', 'Lead the development and launch of new products.', 90000.00);

INSERT INTO application_questions (posting_id, question_text)
VALUES ('POST001', 'Why should we consider you for this position?');

INSERT INTO application_questions (posting_id, question_text)
VALUES ('POST001', 'What is your highest level of education?');

INSERT INTO application_questions (posting_id, question_text)
VALUES ('POST001', 'What is something you have worked on that you are proud of?');

INSERT INTO application_questions (posting_id, question_text)
VALUES ('POST001', 'Please write down your previous work experience.');

INSERT INTO application_answers (profile_id, posting_id, question_id, response_text)
VALUES ('USER001', 'POST001', 1, 'I have a strong background in software engineering and have worked on several high-profile projects.');

INSERT INTO application_answers (profile_id, posting_id, question_id, response_text)
VALUES ('USER001', 'POST001', 2, 'I have a Bachelor''s degree in Computer Science.');

INSERT INTO application_answers (profile_id, posting_id, question_id, response_text)
VALUES ('USER001', 'POST001', 3, 'I recently led a team to successfully launch a new software product.');

INSERT INTO application_answers (profile_id, posting_id, question_id, response_text)
VALUES ('USER001', 'POST001', 4, 'I have 5 years of experience as a software engineer at a leading tech company.');