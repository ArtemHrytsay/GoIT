DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS disciplines;
DROP TABLE IF EXISTS teachers;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS groups;

-- Creating groups table
CREATE TABLE groups (
    id INTEGER PRIMARY KEY,
    group_name VARCHAR(10) NOT NULL
);

-- Creating students table with a foreign key referencing groups
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    group_id INT,
    FOREIGN KEY (group_id) REFERENCES groups(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Creating teachers table
CREATE TABLE teachers (
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);

-- Creating disciplines table with a foreign key referencing teachers
CREATE TABLE disciplines (
    id INTEGER PRIMARY KEY,
    discipline_name VARCHAR(50) NOT NULL,
    teacher_id INT,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Creating grades table with foreign keys referencing students and disciplines
CREATE TABLE grades (
    id INTEGER PRIMARY KEY,
    student_id INT NOT NULL,
    discipline_id INT NOT NULL,
    grade INT CHECK (grade BETWEEN 1 AND 5),
    grade_date DATE NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (discipline_id) REFERENCES disciplines(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
