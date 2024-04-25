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
    company_bio VARCHAR(128),
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
    profile_id VARCHAR(16) NOT NULL,
    institution_name VARCHAR(128) NOT NULL,
    education_level education_level NOT NULL,
    study_area VARCHAR(64) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    PRIMARY KEY (profile_id, institution_name, education_level, start_date),
    FOREIGN KEY (profile_id) REFERENCES user_account(profile_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS job_posting (
    posting_id VARCHAR(24),
    company_id VARCHAR(16) NOT NULL,
    job_title VARCHAR(64) NOT NULL,
    description TEXT NOT NULL,
    salary FLOAT NOT NULL,
    posting_date timestamp DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (posting_id, company_id),
    FOREIGN KEY (company_id) REFERENCES company_account(company_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS posting_tags (
    
);

INSERT INTO company_account (company_id, login, pass, name, company_image, company_banner, company_bio, is_auth)
VALUES ('1', 'comp', 'abc', 'theman', 'image', 'image', 'this is a real comp', true),
VALUES ('2', 'joke', '123', 'Prolific Portrayol', 'clown', 'improv', 'Improv group who never says no ;)', true),
VALUES ('3', 'hire', 'xyz', 'Boston Consoling Group', 'group_hug', 'therapy office', 'Not to be confused with the consulting company', true),
VALUES ('4', 'live', 'wire', 'School of Hard Rock', 'concert', 'guitar hero 3', 'We are here to rock!', true);


INSERT INTO job_posting (posting_id, company_id, job_title, description, salary)
VALUES ('POST001', 'COMP001', 'Software Engineer', 'We are seeking a highly skilled software engineer to join our dynamic team.', 80000.00);
VALUES ('POST002', 'COMP002', 'Data Analyst', 'We are looking for a talented data analyst to help us analyze and interpret data.', 60000.00);
VALUES ('POST003', 'COMP003', 'Marketing Manager', 'Join our marketing team and lead strategic marketing initiatives.', 70000.00);
VALUES ('POST004', 'COMP004', 'Graphic Designer', 'Create stunning visuals and designs for our marketing campaigns.', 55000.00);
VALUES ('POST005', 'COMP002', 'Business Development Manager', 'Drive business growth through strategic partnerships and initiatives.', 75000.00);
VALUES ('POST006', 'COMP001', 'Product Manager', 'Lead the development and launch of new products.', 90000.00);




