-- ==============================
-- DROP TABLES TO AVOID COLLISIONS
-- Drop all tables in correct dependency order so no conflicts occur
-- ==============================
DROP TABLE IF EXISTS notes_comments;
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS grades_temp;

-- ==============================
-- CREATE SUBJECTS TABLE
-- Holds subjects to avoid hardcoding them elsewhere
-- ==============================
CREATE TABLE IF NOT EXISTS subjects (
    id SERIAL PRIMARY KEY,               -- Auto incrementing unique ID
    name VARCHAR(30) UNIQUE NOT NULL    -- Subject name must be unique and not null
);

-- ==============================
-- INSERT SUBJECT NAMES
-- Insert initial subject names, ignoring duplicates if rerun
-- ==============================
INSERT INTO subjects (name) VALUES
    ('Math'),
    ('English'),
    ('German'),
    ('Science'),
    ('History'),
    ('Biology')
ON CONFLICT (name) DO NOTHING;         -- Prevent duplicate insert errors

-- ==============================
-- CREATE STUDENTS TABLE
-- Store student information including name, email, class, and overall grade
-- ==============================
CREATE TABLE students (
    id SERIAL PRIMARY KEY,                  -- Auto incrementing student ID
    name VARCHAR(100) NOT NULL,             -- Student full name, mandatory
    email VARCHAR(100) UNIQUE,              -- Email must be unique if provided
    class_number VARCHAR(5),                -- Class number, e.g. "12B"
    overall_grade VARCHAR(1)                -- Overall grade with allowed values
        CHECK (overall_grade IN ('A','B','C','D','F'))
);

-- ==============================
-- INSERT STUDENT DATA
-- Add initial students with their details
-- ==============================
INSERT INTO students (name, email, class_number, overall_grade)
VALUES
    ('Mason Davis', 'mason.davis879@gmail.com', '11C', 'B'),
    ('Sophia Miller', 'sophia.miller204@gmail.com', '11C', 'A'),
    ('Ethan Wilson', 'ethan.wilson377@gmail.com', '11C', 'C'),
    ('Isabella Moore', 'isabella.moore112@gmail.com', '11C', 'D'),
    ('James Taylor', 'james.taylor633@gmail.com', '11C', 'B'),
    ('Liam Smith', 'liam.smith123@gmail.com', '12B', 'A'),
    ('Emma Johnson', 'emma.johnson456@gmail.com', '12B', 'B'),
    ('Noah Williams', 'noah.williams789@gmail.com', '12B', 'A'),
    ('Olivia Brown', 'olivia.brown321@gmail.com', '12B', 'D'),
    ('Ava Jones', 'ava.jones654@gmail.com', '12B', 'C');

-- ==============================
-- CREATE GRADES TABLE
-- Track grades per student and subject
-- ==============================
CREATE TABLE grades (
    id SERIAL PRIMARY KEY,                      -- Auto incrementing grade record ID
    student_id INTEGER REFERENCES students(id), -- FK referencing students
    subject_id INTEGER REFERENCES subjects(id), -- FK referencing subjects
    grade VARCHAR(1) CHECK (grade IN ('A','B','C','D','F')), -- Allowed grades only
    graded_on DATE DEFAULT CURRENT_DATE          -- Date when grade was assigned
);

-- ==============================
-- INSERT SAMPLE GRADES
-- Using subject IDs instead of names (e.g. Math=1)
-- ==============================
INSERT INTO grades (student_id, subject_id, grade) VALUES
    (1, 1, 'A'),   
    (2, 2, 'B'),   
    (3, 3, 'C'),    
    (4, 4, 'B'),   
    (5, 5, 'D'),    
    (6, 6, 'A'),    
    (7, 1, 'C'),    
    (8, 2, 'B'),    
    (9, 3, 'A'),    
    (10, 4, 'F');   
	 
-- ==============================
-- CREATE ATTENDANCE TABLE
-- Track daily attendance for students
-- ==============================
CREATE TABLE attendance (
    id SERIAL PRIMARY KEY,                      -- Attendance record ID
    student_id INTEGER REFERENCES students(id), -- FK to student
    attendance_date DATE NOT NULL DEFAULT CURRENT_DATE, -- Attendance date, defaults to today
    attendance BOOLEAN NOT NULL DEFAULT FALSE,   -- Present (TRUE) or Absent (FALSE)
    UNIQUE(student_id, attendance_date)          -- Prevent duplicate attendance for same day/student
);

-- ==============================
-- INSERT ATTENDANCE DATA
-- Sample attendance marking
-- ==============================
INSERT INTO attendance (student_id, attendance) VALUES
    (1, TRUE),
    (2, FALSE),
    (3, TRUE),
    (4, TRUE),
    (5, FALSE),
    (6, TRUE),
    (7, FALSE),
    (8, TRUE),
    (9, TRUE),
    (10, FALSE);
    
-- ==============================
-- CREATE NOTES/COMMENTS TABLE
-- For observations or warnings about students
-- ==============================
CREATE TABLE notes_comments (
    id SERIAL PRIMARY KEY,                      -- Unique ID for comment
    student_id INTEGER REFERENCES students(id) ON DELETE CASCADE, -- FK, delete comments if student deleted
    comment TEXT NOT NULL,                      -- The comment text, mandatory
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp of comment creation
);

-- ==============================
-- INSERT SAMPLE COMMENTS
-- ==============================
INSERT INTO notes_comments (student_id, comment) VALUES
    (1, 'Liam is a bright student, but can be lazy sometimes...'),
    (2, 'Sophia has shown great improvement this term.'),
    (3, 'Noah has seafood allergies and can’t play PE today.'),
    (4, 'Isabella is very attentive in class.'),
    (5, 'James needs to participate more actively.'),
    (6, 'Emma excels in Mathematics and Science.'),
    (7, 'Olivia sometimes struggles with deadlines.'),
    (8, 'Ava is very helpful to her classmates.'),
    (9, 'Mason shows excellent teamwork skills.'),
    (10, 'Ethan has been absent a few times this month.');

-- ==============================
-- CREATE GRADES_TEMP TABLE
-- Acts as a staging/manual review table for grades imported from CSV
-- ==============================
CREATE TABLE IF NOT EXISTS grades_temp (
    student_id INTEGER,                         -- Student ID (to be validated)
    subject_name VARCHAR(30),                   -- Subject name (to be validated)
    grade VARCHAR(2)                            -- Grade value (to be validated)
);

-- ==============================
-- CLEAN UP grades_temp TABLE
-- Remove any previous data before importing new CSV data
-- ==============================
TRUNCATE TABLE grades_temp;

-- ==============================
-- LOAD CSV DATA INTO grades_temp
-- Modify the file path as needed for your environment
-- ==============================
COPY grades_temp(student_id, subject_name, grade)
FROM 'C:\Users\User\OneDrive\Desktop\SGS2.csv'
WITH (
    FORMAT csv,
    HEADER,
    DELIMITER ','
);

-- ==============================
-- ADD validation_status COLUMN IF NOT EXISTS
-- This column flags validity of each imported row
-- ==============================
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'grades_temp' AND column_name = 'validation_status'
    ) THEN
        ALTER TABLE grades_temp ADD COLUMN validation_status VARCHAR(20);
    END IF;
END $$;

-- ==============================
-- UPDATE validation_status BASED ON RULES
-- Check if student_id exists, subject_name exists, and grade is valid
-- ==============================
UPDATE grades_temp
SET validation_status = CASE
    WHEN student_id NOT IN (SELECT id FROM students) THEN 'Invalid student_id'
    WHEN subject_name NOT IN (SELECT name FROM subjects) THEN 'Invalid subject_name'
    WHEN grade NOT IN ('A', 'B', 'C', 'D', 'F') THEN 'Invalid grade'
    ELSE 'Valid'
END;

-- ==============================
-- DISPLAY ALL DATA FROM grades_temp
-- Shows all rows with their validation status for review
-- ==============================
SELECT * FROM grades_temp;
