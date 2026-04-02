DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS programs;
DROP TABLE IF EXISTS colleges;
DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users(
    username    VARCHAR(20)     PRIMARY KEY,
    password    VARCHAR(255)    NOT NULL,
    role        VARCHAR(20)     NOT NULL        DEFAULT 'user'
);

CREATE TABLE IF NOT EXISTS colleges(    
    college_code    VARCHAR(8)      PRIMARY KEY,
    college_name    VARCHAR(50)     NOT NULL
);

CREATE TABLE IF NOT EXISTS programs(
    program_code    VARCHAR(8)      PRIMARY KEY,
    program_name    VARCHAR(50)     NOT NULL,
    college_code    VARCHAR(8)      NOT NULL,
    FOREIGN KEY (college_code)      REFERENCES      colleges(college_code)
);

CREATE TABLE IF NOT EXISTS students (
    student_id              VARCHAR(9)              PRIMARY KEY, /*Format: 1234-5678 */
    student_first_name      VARCHAR(255)            NOT NULL,
    student_last_name       VARCHAR(255)            NOT NULL,
    gender                  ENUM('Male', 'Female')  NOT NULL,
    student_year_level      ENUM('1', '2', '3', '4')NOT NULL,
    program_code            VARCHAR(8)              NOT NULL,
    FOREIGN KEY (program_code)  REFERENCES          programs(program_code)
);

INSERT INTO colleges (college_code, college_name) VALUES
    ('CCS', 'College of Computer Studies'),
    ('CBA', 'College of Business Administration');

INSERT INTO programs (program_code, program_name, college_code) VALUES
    ('BSCS', 'BS Computer Science', 'CCS'),
    ('BSCA', 'BS Computer Application', 'CCS'),
    ('BSIT', 'BS Information Technology', 'CCS');

INSERT INTO students (student_id, student_first_name, student_last_name, gender, student_year_level, program_code) VALUES
    ('2021-0001', 'Joshua', 'Cruz', 'Male', 3, 'BSCS'),
    ('2021-0002', 'Michael', 'Lee', 'Male', 2, 'BSCS'),
    ('2021-0003', 'Tom', 'Peaky', 'Male', 1, 'BSIT');

DELETE FROM users WHERE username = 'admin';

SELECT * FROM users;

INSERT INTO users (username, password, role) VALUES
    ('admin', 'admin', 'admin');

UPDATE users SET role = 'admin' WHERE username = 'admin';