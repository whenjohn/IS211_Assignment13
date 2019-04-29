#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sqlite3 as lite
import time

datetime = time.time()


student_list = (
    ("James", "Blake"),
    ("Sarah", "Smith"),
    ("Joe", "Smyth"),
)

quiz_list = (
    ("Python Basics", 5, "11-8-2019"),
    ("Python Advance", 5,  "11-9-2019"),
)


quiz_result = (
    (1, 1, 88),
    (2, 1, 95),
    (1, 2, 79),
)
con = lite.connect('hw13')
with con:
    cur = con.cursor()

################### Create Students Table ##############################
#    cur.execute("DROP TABLE IF EXISTS tbl_students")
#    cur.execute("CREATE TABLE tbl_students (sid INTEGER PRIMARY KEY ASC, fname TEXT, lname TEXT)")
#    cur.executemany("INSERT INTO tbl_students (fname, lname) VALUES(?, ?)", student_list)
#    con.commit()


################### Create Quiz Table ##############################
    cur.execute("DROP TABLE IF EXISTS tbl_quizzes")
    cur.execute("CREATE TABLE tbl_quizzes (qid INTEGER PRIMARY KEY ASC, subject TEXT, num_questions INT, date_given TEXT)")
    cur.executemany("INSERT INTO tbl_quizzes (subject, num_questions, date_given) VALUES(?, ?, ?)", quiz_list)
    con.commit()

################### Create Quiz Results Table ##############################
#    cur.execute("DROP TABLE IF EXISTS tbl_quiz_results")
#    cur.execute("CREATE TABLE tbl_quiz_results (sid INT, qid INT, score INT)")
#    cur.executemany("INSERT INTO tbl_quiz_results (sid, qid, score) VALUES(?, ?, ?)", quiz_result)
#    con.commit()
