from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from random import shuffle
from models import db, Quiz, Question, db_add_new_data

BASE_DIR = os.getcwd()
BASE_DIR = os.path.join(BASE_DIR, 'HW9')
DB_PATH = os.path.join(BASE_DIR, 'db', 'db_quiz.db')
print('путь:',DB_PATH)

app = Flask(__name__, template_folder=os.path.join(BASE_DIR,'templates'))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SECRET_KEY'] = 'sfsdf12313xcvxcDD/\,'

db.init_app(app)

with app.app_context():
    db_add_new_data()

    quizes = Quiz.query.order_by(Quiz.name.desc()).all()
    #print(quizes)
    for quiz in quizes:
        print(quiz)
        print(quiz.question)


    question = Question.query.all()
    print(question)    

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        quizes = Quiz.query.all()
        return render_template('start.html', quizes=quizes)
    session['quiz_id'] = request.form.get('quiz')
    session['question_n'] = 0
    redirect(url_for('question'))



@app.route('question', methods = ['GET', 'POST'])
def question():
    if not session['quiz_id'] or session['quiz_id'] < 0:
        redirect(url_for('index'))
    quiz = Quiz.query.filter_by(id = session['quiz_id'])
    if int(session['question_n']) >= len(quiz[0].question):
        redirect(url_for('result'))
    else:
        question = quiz[0].question[session['question_n']]
        answers = [question.answer, question.wrong1, question.wrong2, question.wrong3]
        shuffle(answers)
        return(render_template('question.html'), answers=answers, qustion=question)    


@app.route('/questions/')
def view_questions():
    questions = Question.query.all()
    return render_template('questions.html', questions = questions)


app.run(debug=True)    