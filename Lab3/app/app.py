from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from faker import Faker

fake = Faker()

app = Flask(__name__)
application = app

app.config.from_pyfile('config.py') 

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'
login_manager.login_message = 'Войдите в аккаунт для доступа к материалам сайта)'
login_manager.login_message_category = 'warning'

def get_users():
    return [
        {
            'id': '1',
            'login': 'user',
            'password': 'qwerty'
        }
    ]

@login_manager.user_loader
def load_user(user_id):
    for user in get_users():
        if user_id == user['id']:
            return User(user['id'], user['login'])
    return None

class User(UserMixin):
    def __init__(self, user_id, login):
        self.id = user_id
        self.login = login
        
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    next_page = request.args.get('next')
    
    if request.method == 'POST':
        login = request.form.get('username')
        password = request.form.get('password')
        check = request.form.get('remember_me') == 'on'
        if login and password:
            for user in get_users():
                if user['login'] == login and user['password'] == password:
                    user = User(user['id'], user['login'])
                    login_user(user, remember = check)
                    flash('Вы успешно аутентифицированы!', 'success')
                    session['greeting'] = "Добро пожаловать, " + login + "!"
                    return redirect(next_page or url_for('index'))
            return render_template('login.html', error="Введены неверные данные!")
        return render_template('login.html', error="Необходимо заполнить все поля!")
    return render_template('login.html')
    

@app.route('/visitscounter')
def visitscounter():
    
    if current_user.is_authenticated:
        if session.get(current_user.login):
            session[current_user.login] += 1
            session['counter'] = 1 if session.get('counter') else session['counter'] + 1
        else:
            session[current_user.login] = 1
            session['counter'] = 1 if session.get('counter') else session['counter'] + 1
    else:
        if session.get('counter'):
            session['counter'] += 1
        else:
            session['counter'] = 1
    
    return render_template('visitscounter.html')

@app.route('/secretpage')
@login_required
def secretpage():
    return render_template('secretpage.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))