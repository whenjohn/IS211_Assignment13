CREATE TABLE tbl_students (sid INTEGER PRIMARY KEY ASC, fname TEXT, lname TEXT);

CREATE TABLE tbl_quizzes (sid INTEGER PRIMARY KEY ASC, subject TEXT, num_questions INT, date_given REAL);

CREATE TABLE tbl_quiz_results (sid INT, qid INT, score INT);
