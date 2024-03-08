#from typing import Any
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    # __tablename__ = user
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(25))
    quizes = db.relationship('Quiz', backref='user')

    def __init__(self, name) -> None:
        super().__init__()
        self.name = name



class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name: str, user:User) -> None:
        super().__init__()
        self.name = name
        self.user = user

    def __repr__(self) -> str:
        return f'id - {self.id}, name - {self.name}'



quiz_question = db.Table('quiz_question',
            db.Column('quiz_ud', db.Integer, db.ForeignKey('quiz.id')),
            db.Column('question_id', db.Integer, db.ForeignKey('question.id')),
            )


class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.String(250), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    wrong1 = db.Column(db.String(100), nullable=False)
    wrong2 = db.Column(db.String(100), nullable=False)
    wrong3 = db.Column(db.String(100), nullable=False)
    quiz = db.relationship('Quiz', secondary=quiz_question, backref = 'question')

    def __init__(self, quesion: str, answer, wrong1, wrong2, wrong3) -> None:
        super().__init__()
        self.question = quesion
        self.answer = answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3

    def __repr__(self):
        return f'{self.question}'


def db_add_quiz(quiz_name: str):
    quiz = Quiz(quiz_name, None)
    db.session.add(quiz)
    db.session.commit()

def db_edit_quiz(quiz_id: int, quiz_name: str, questions_checked: list):
    quiz = Quiz.query.get(quiz_id)
    quiz.name = quiz_name
    questions = Question.query.all()
    print(f'вопросы в квизе {quiz.question}',)
    print(f'Все вопросы {questions}',)
    for id_checked in questions_checked:
        for question in questions:
            print(f'quiz.question =  {quiz.question}')
            if question.id == int(id_checked) and question not in quiz.question:
                print(f'Дабавляем вопрос {question} c id {id_checked}',)
                quiz.question.append(question)
            elif question.id == int(id_checked) and question in quiz.question:
                print("Вопрос уже включен")
            else:
                if question in quiz.question:
                    print(f'Удаляем вопрос {question} c id {id_checked}',)
                    quiz.question.remove(question)  
    print(quiz.question)
    db.session.add(quiz)
    db.session.commit()


def db_add_question(question_name: str, question_answer: str, question_wrong1: str, question_wrong2: str, question_wrong3: str):
    question = Question(question_name, question_answer, question_wrong1, question_wrong2, question_wrong3)
    db.session.add(question)
    db.session.commit()

def db_edit_question(question_id: int, question_question: str, question_answer: str, question_wrong1: str, question_wrong2: str, question_wrong3: str):
    question = Question.query.get(question_id)
    print(f'question.question = {question.question}, question_question = {question_question}')
    question.question = question_question
    question.answer = question_answer
    question.wrong1 = question_wrong1
    question.wrong2 = question_wrong2
    question.wrong3 = question_wrong3
    db.session.add(question)
    db.session.commit()






# def db_add_quiz(quiz_name: str,user_id: int, questions_id):

#     user = User.query.get(user_id)
#     quiz = Quiz(quiz_name,user)
#     db.session.add(quiz)
#     db.session.commit()
#     for question_id in questions_id:
#         print('Вопрос id',question_id)
#         question_id = int(question_id)
#         #question_id = Question.query.get(question_id)   
#         print('Вопрос id', question_id)
#         print('Квиз id:',quiz.id)
#         data = quiz_question.select()
#         print(data)
#         quiz_question.add_is_dependent_on(quiz.id,question_id) 
#     db.session.add(quiz)
#     #db.session.add(quiz_question)
#     db.session.commit()


def db_add_new_data():
    db.drop_all()
    db.create_all()

    user1 = User('user1')
    user2 = User('user2')


    quizes = [
        Quiz('QUIZ 1', user1),
        Quiz('QUIZ 2', user1),
        Quiz('QUIZ 3', user2),
        Quiz('QUIZ 4', user2)
    ]


    questions = [
        Question('Сколько будут 2+2*2', '6', '8', '2', '0'),
        Question('Сколько месяцев в году имеют 28 дней?', 'Все', 'Один', 'Ни одного', 'Два'),
        Question('Каким станет зелёный утёс, если упадет в Красное море?', 'Мокрым?', 'Красным', 'Не изменится', 'Фиолетовым'),
        Question('Какой рукой лучше размешивать чай?', 'Ложкой', 'Правой', 'Левой', 'Любой'),
        Question('Что не имеет длины, глубины, ширины, высоты, а можно измерить?', 'Время', 'Глупость', 'Море', 'Воздух'),
        Question('Когда сетью можно вытянуть воду?', 'Когда вода замерзла', 'Когда нет рыбы', 'Когда уплыла золотая рыбка', 'Когда сеть порвалась'),
        Question('Что больше слона и ничего не весит?', 'Тень слона', 'Воздушный шар', 'Парашют', 'Облако'),
        Question('Что такое у меня в кармашке?', 'Кольцо', 'Кулак', 'Дырка', 'Бублик')
    ]

    quizes[0].question.append(questions[0])
    quizes[0].question.append(questions[1])
    quizes[0].question.append(questions[2])
    
    
    quizes[1].question.append(questions[3])
    quizes[1].question.append(questions[4])
    quizes[1].question.append(questions[5])
    quizes[1].question.append(questions[6])
    quizes[1].question.append(questions[0])
    
    quizes[2].question.append(questions[7])
    quizes[2].question.append(questions[6])
    quizes[2].question.append(questions[5])
    quizes[2].question.append(questions[4])
    
    quizes[3].question.append(questions[6])
    quizes[3].question.append(questions[0])
    quizes[3].question.append(questions[1])
    quizes[3].question.append(questions[3])





    db.session.add_all(quizes)
    db.session.commit()
