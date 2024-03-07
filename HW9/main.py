#pip install flask-sqlalchemy

from flask import Flask, redirect, render_template, request, session, url_for
import os
from models import db, Quiz, Question, db_add_new_data, db_add_quiz, db_edit_quiz, User
from random import shuffle

BASE_DIR = os.getcwd()

DB_PATH = os.path.join(BASE_DIR, 'db', 'db_quiz.db')

app = Flask(__name__, 
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SECRET_KEY'] = 'secretkeysecretkeysecretkey1212121'

db.init_app(app)



with app.app_context():
    db_add_new_data()

    # quizes = Quiz.query.order_by(Quiz.name.desc()).all()
    # for q in quizes:
    #     print(f"{q}")
    #     for qu in q.question:
    #         print('-'*5, qu)

    # question = Question.query.filter_by(id=2).all()
    


@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'GET':
        session['quiz_id'] = -1
        quizes = Quiz.query.all()
        return render_template('start.html', quizes=quizes)
    session['quiz_id'] = request.form.get('quiz')
    session['question_n'] = 0
    session['question_id'] = 0
    session['right_answers'] = 0
    return redirect(url_for('question'))


@app.route('/question/', methods = ['POST', 'GET'])
def question():
    
    if not session['quiz_id'] or session['quiz_id'] == -1:
        return redirect(url_for('index'))

    # если пост значит ответ на вопрос        
    if request.method == 'POST':        
        question = Question.query.filter_by(id=session['question_id']).all()[0]        
        # если ответ ы сходятся значит +1
        if question.answer == request.form.get('ans_text'):
            session['right_answers'] += 1
        # следующий вопрос
        session['question_n'] += 1


    quiz = Quiz.query.filter_by(id = session['quiz_id']).all()
    if int(session['question_n']) >= len(quiz[0].question):
        session['quiz_id'] = -1 # чтообы больше не работола страница question
        return redirect(url_for('result'))
    
    else:
        question = quiz[0].question[session['question_n']]
        session['question_id'] = question.id
        answers = [question.answer, question.wrong1, question.wrong2, question.wrong3 ]
        shuffle(answers)

        return render_template('question.html', answers=answers, question=question)



@app.route('/questions/')
def vew_questions():
    questions = Question.query.all()
    print(questions)
    return render_template('questions.html', questions = questions)

@app.route('/add_question/')
def add_question():
    pass


@app.route('/result/')
def result():
    return render_template('result.html', 
                    right=session['right_answers'], 
                    total = session['question_n'])

#add
# @app.route('/add_quiz/', methods = ['POST', 'GET'])
# def add_quiz():
#     if request.method == 'GET': 
#         print(1)
#         users = User.query.all()
#         questions = Question.query.all()
#         return render_template('quiz.html', users=users, questions=questions)
#     if request.method == 'POST': 
#         print(2)
#         quiz = request.form.get('quiz')
#         user_id = int(request.form.get('user'))
#         questions = request.form.getlist('questions')
#         print(quiz, user_id)
#         print("Вопросы", questions)
#         with app.app_context():
#             db_add_quiz(quiz, user_id, questions)
#         return redirect(url_for('view_quizes'))

@app.route('/add_quiz/', methods = ['POST'])
def add_quiz():

    quiz = request.form.get('quiz_name')
    print(quiz)
    with app.app_context():
        db_add_quiz(quiz)
    return redirect(url_for('view_quizes'))

@app.route('/edit_quiz/', methods = ['GET', 'POST'])
def edit_quiz():
    if request.method == 'GET':  
        print("GET methodos")
        quiz_id = request.args.get('quiz_id')
        print("КВИЗ = ", quiz_id)
        # quiz = Quiz.query.filter_by(id = quiz_id).all()
        #quiz = Quiz.query.filter(Quiz.id == quiz_id).all()
        quiz = Quiz.query.get(quiz_id)
        print("КВИЗ all = ", quiz)
        print(quiz.id, quiz.name)
        return render_template('edit_quiz.html', quiz_id = quiz.id, quiz_name = quiz.name)
    if request.method == 'POST':  
        try:
            quiz_id = request.form.get('quiz_id')
        except:
            return redirect(url_for('view_quizes'))    
        quiz_name = request.form.get('quiz_name')
        with app.app_context():
            db_edit_quiz(quiz_id, quiz_name)
        return redirect(url_for('view_quizes'))


@app.route('/quizes/')
def view_quizes():
    quizes = Quiz.query.all()
    users = User.query.all()
    print(*quizes,sep='/n')
    print(*users,sep='/n')
    return render_template('quizes.html', quizes = quizes, users=users)



app.run(debug=True)