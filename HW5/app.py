from flask import Flask, request, redirect, render_template, \
                  send_from_directory, url_for
import os
from werkzeug.utils import secure_filename


BASE_DIR = os.getcwd()
BASE_DIR += '\HW5'
print(BASE_DIR)

app = Flask(__name__, static_folder=os.path.join(BASE_DIR,'static'),
            template_folder=os.path.join(BASE_DIR,'templates')
            )

app.config['SECRET_KEY'] = 'weklj23hk12k3KJHKJK'

users = ['user1','user2','user3','user4',]

@app.route('/')
def index():
    s = '<h4>Пользователи</h4>'
    for user in users:
        s += f'<p> Пользователь: {user}</p>'
    return s

@app.route('/users/')
def index_user():
    return render_template('1.html', users=users, head='Администраторы', q=1, color='red')


if __name__ == "__main__":
    app.run(debug=True)