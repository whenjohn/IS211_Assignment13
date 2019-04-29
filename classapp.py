# classapp.py

from flask import request, redirect, url_for, Flask, render_template, session
import sqlite3 as lite
import time

app = Flask(__name__)
app.secret_key = "Th1si5@53cret"


@app.route('/')
def index():
    session.clear()
    return render_template('index.html')


@app.route('/anon')
def set_anon():
    session['username'] = "Anonymous"
    session.modified = True
    return redirect(url_for('dashboard'))


@app.route('/login', methods = ['POST'])
def login():
    if request.form['state'] == "enter":
        return render_template('login.html')
    elif request.form['user'] == "admin" and request.form['password'] == "password":
        session['username'] = "Admin"
        session.modified = True
        return redirect(url_for('dashboard'))
    else:
        error="Enter correct credentials"
        return render_template('login.html', error=error)


@app.route('/dashboard')
def dashboard():
    return_student_list = getStudentList()
    return_quiz_list = getQuizList()
    return render_template('dashboard.html', username=session['username'], student_list=return_student_list, quiz_list=return_quiz_list)

def getStudentList():
    con = lite.connect('hw13')
    cur = con.cursor()
    cur.execute("SELECT * FROM tbl_students;")
    return cur.fetchall()

def getQuizList():
    con = lite.connect('hw13')
    cur = con.cursor()
    cur.execute("SELECT * FROM tbl_quizzes ORDER BY qid asc;")
    return cur.fetchall()


@app.route('/student/<action>', methods=['GET', 'POST'])
def student (action):
    if request.method == 'POST':
        error = None
        for value in request.values:
            if request.values.get(value) == "":
                error = "Enter correct value"
        if error:
            return render_template('student_add.html', error=error)
        else:
            addStudent(request.values.get('fname'), request.values.get('lname'))
            return redirect(url_for('dashboard'))
    else:
        if action == "form":
            return render_template('student_add.html')
        if action == "delete":
            deleteStudent(request.args.get('id'))
            return redirect(url_for('dashboard'))
        else:
            if request.args.get('del'):
                sid = action
                qid = request.args.get('del')
                deleteQuizResults(sid,qid)
                return redirect(url_for('dashboard'))
            else:
                return_student_results = getStudentResults(action)
                return render_template('student.html', student_results=return_student_results)

def getStudentResults(sid):
    con = lite.connect('hw13')
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM tbl_quiz_results INNER JOIN tbl_quizzes ON tbl_quiz_results.qid = tbl_quizzes.qid WHERE tbl_quiz_results.sid=? ;", (sid,))
    return cur.fetchall()

def addStudent(fname,lname):
    con = lite.connect('hw13')
    cur = con.cursor()
    cur.execute("INSERT INTO tbl_students (fname, lname) VALUES(?, ?)", (fname,lname))
    con.commit()


@app.route('/quiz/<action>', methods=['GET', 'POST'])
def quiz (action):
    if request.method == 'POST':
        error = None
        for value in request.values:
            if request.values.get(value) == "":
                error = "Enter correct value"
        if error:
            return render_template('quiz_add.html', error=error)
        else:
            addQuiz(request.values.get('subject'),request.values.get('num_questions'),request.values.get('month'),request.values.get('day'),request.values.get('year'))
            return redirect(url_for('dashboard'))
    else:
        if action == "delete":
            deleteQuiz(request.args.get('id'))
            return redirect(url_for('dashboard'))
        elif action == "add":
            return render_template('quiz_add.html')
        else:

            return_quiz_results = getQuizResults(action)
            print return_quiz_results
            return render_template('quiz.html',  username=session['username'], quiz_results=return_quiz_results)

def addQuiz(subject,num_q,mon,day,yr):
    quiz_list = (subject,num_q,(mon+"-"+day+"-"+yr))
    con = lite.connect('hw13')
    cur = con.cursor()
    cur.execute("INSERT INTO tbl_quizzes (subject, num_questions, date_given) VALUES(?, ?, ?)", quiz_list)
    con.commit()

def getQuizResults(qid):
    con = lite.connect('hw13')
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM tbl_quiz_results INNER JOIN tbl_students ON tbl_quiz_results.sid = tbl_students.sid WHERE tbl_quiz_results.qid=? ;", (qid,))
    return cur.fetchall()


@app.route('/results/<action>', methods=['GET', 'POST'])
def results (action):
    return_quiz_list = None
    selected = None
    return_student_list = getStudentList()

    if request.method == 'POST':
        error = None
        selected = request.values.get('student')
        return_quiz_list = getQuizAvailableForStudent(selected)

        if request.values.get('btn') == "btn_submit":
            for value in request.values:
                if request.values.get(value) == "":
                    error = "Enter correct value"

            if error:
                return render_template('quiz_results_add.html', student_list=return_student_list, quiz_list=return_quiz_list, selected=selected, error=error)
            else:
                addResult(request.values.get('student'),request.values.get('quiz'),request.values.get('score'))
                return redirect(url_for('dashboard'))

    return render_template('quiz_results_add.html', student_list=return_student_list, quiz_list=return_quiz_list, selected=selected)

def addResult(sid,qid,score):
    con = lite.connect('hw13')
    cur = con.cursor()
    cur.execute("INSERT INTO tbl_quiz_results (sid, qid, score) VALUES(?, ?, ?)", (sid,qid,score))
    con.commit()

def getQuizAvailableForStudent(sid):
    # get all quiz in dict
    quiz_list = getQuizList()
    quiz_set = []
    for quiz in quiz_list:
        quiz_set.append(quiz[0])

    # get all qid where studentid, store in set
    student_quiz_list = getStudentResults(sid)
    student_set = []
    for student in student_quiz_list:
        student_set.append(student[1])

    # - operator on set, covert to List
    diff_quizid_list = list(set(quiz_set)-set(student_set))

    # recreate new quiz list from diffs
    new_quiz_list = []
    for pos in range(len(diff_quizid_list)):
        for quiz in quiz_list:
            if diff_quizid_list[pos] == quiz[0]:
                new_quiz_list.append((quiz[0], quiz[1]))
                break
    return new_quiz_list

def deleteStudent(id):
    con = lite.connect('hw13')
    cur = con.cursor()
    cur.execute("DELETE FROM tbl_students WHERE sid=? ;", (id,))
    cur.execute("DELETE FROM tbl_quiz_results WHERE sid=? ;", (id,))
    con.commit()

def deleteQuiz(id):
    con = lite.connect('hw13')
    cur = con.cursor()
    cur.execute("DELETE FROM tbl_quizzes WHERE qid=? ;", (id,))
    cur.execute("DELETE FROM tbl_quiz_results WHERE qid=? ;", (id,))
    con.commit()

def deleteQuizResults(sid,qid):
    con = lite.connect('hw13')
    cur = con.cursor()
    cur.execute("DELETE FROM tbl_quiz_results WHERE sid=? AND qid=? ;", (sid,qid,))
    con.commit()


if __name__ == "__main__":
    app.run()
