from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
import random

app = Flask(__name__)

mydb = mysql.connector.connect(
    host = "localhost", 
    user = "root",
    passwd = "Ahamed@@122",
    database = "quiz"
)

mycursor = mydb.cursor()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/add_question", methods=["GET", "POST"])
def add_question():
    if request.method == "POST":
        question = request.form["question"]
        option1 = request.form["option1"]
        option2 = request.form["option2"]
        option3 = request.form["option3"]
        option4 = request.form["option4"]
        correct = request.form["answer"]

        mycursor.execute("INSERT INTO all_questions(questions, option1, option2, option3, option4, answer) VALUES(%s, %s, %s, %s, %s, %s)",(question, option1, option2, option3, option4, correct))
        mydb.commit()
        return redirect(url_for("home"))
    return render_template("add_question.html")

@app.route("/quiz", methods=["POST", "GET"])
def quiz():
    if request.method == "POST":
        name = request.form["name"]
        mycursor.execute("SELECT * from all_questions")
        data = mycursor.fetchall()
        
        total_questions = len(data)
        question_indexes = random.sample(range(total_questions), min(5, total_questions))
        questions = [data[i] for i in question_indexes]
        return render_template("quiz.html", name=name, questions=questions)
    return redirect(url_for("home"))

@app.route("/submit", methods=["POST"])
def submit():
    answers = request.form
    name = answers.get("name")

    score = 0
    wrong = {}

    for qid, ans in answers.items():
        if qid == "name":
            continue
        mycursor.execute("SELECT * from all_questions where qn_id=%s", (qid,))
        qn = mycursor.fetchone()
        if ans == qn[6]:
            score += 1
        else:
            wrong[qn[1]] = qn[6]
        
    mycursor.execute("SELECT * from user_details")
    _ = mycursor.fetchall()
    user_id = mycursor.rowcount + 1
    mycursor.execute("INSERT INTO user_details VALUES(%s, %s, %s)",(user_id, name, score))
    mydb.commit()

    return render_template("result.html", score=score, wrong=wrong, name=name)

if __name__ == "__main__":
    app.run(debug=True)
        

