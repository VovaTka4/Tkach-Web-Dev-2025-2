from functools import wraps
from flask import Blueprint, request, render_template, url_for, redirect, flash
from flask_login  import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from .repositories.user_repository import UserRepository
import mysql.connector as connector
from .db import db
from .validators import password_validator

user_repository = UserRepository(db)

bp = Blueprint('auth', __name__, url_prefix='/auth')

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Авторизуйтесь для доступа к ресурсу.'
login_manager.login_message_category = 'warning'

class User(UserMixin):
    def __init__(self, user_id, login):
        self.id = user_id
        self.login = login

@login_manager.user_loader
def load_user(user_id):
    user = user_repository.get_by_id(user_id)
    if user is not None:
        return User(user.id, user.username)
    return None

@bp.route('/login', methods=['GET', 'POST'])
def login():    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me') == 'on'
        
        user = user_repository.get_by_username_and_password(username, password)
        
        if user is not None:
            flash('Авторизация прошла успешно', 'success')
            login_user(User(user.id, user.username), remember=remember_me)
            next_url = request.args.get('next', url_for('users.index'))
            return redirect(next_url)
        flash('Invalid username or password', 'danger')
    return render_template('auth/login.html')

@bp.route('/register', methods = ['POST', 'GET'])
def register():
    user_data = {}
    passwords_not_matching = None
    validation_error = None
    
    if request.method == 'POST':
        fields = ('username', 'email', 'password', 'password_r')
        user_data = { field: request.form.get(field) or None for field in fields }
        
        if user_data['password'] != user_data['password_r']:
            passwords_not_matching = "Пароли не совпадают!"
        
        validation_error = 'Username должен содержать хотя бы 5 символов!' if (user_data['username'] is None or len(user_data['username']) < 5) else password_validator(user_data['password']) 
        
        if validation_error or passwords_not_matching:
            flash(validation_error, 'danger')
            return render_template('auth/register.html', user_data=user_data, val_error=validation_error, passwords_not_matching=passwords_not_matching)
        
        try:
            user_repository.create(user_data['username'], user_data['email'], user_data['password'], False)
            flash('Учетная запись успешно создана', 'success')
            return redirect(url_for('pages.bmr_calculator'))
        except connector.errors.DatabaseError:
            flash('Произошла ошибка при создании записи. Проверьте, что все необходимые поля заполнены', 'danger')
            db.connect().rollback()
    return render_template('auth/register.html', user_data=user_data, val_error=validation_error, passwords_not_matching=passwords_not_matching)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))