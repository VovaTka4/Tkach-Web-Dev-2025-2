from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
import mysql.connector as connector
from .validators.password_validator import password_validator
from werkzeug.security import check_password_hash, generate_password_hash

from .repositories.user_repository import UserRepository
from .repositories.role_repository import RoleRepository
from .decorators.check_rights import check_rights, has_rights
from .db import db

user_repository = UserRepository(db)
role_repository = RoleRepository(db)

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/')
@check_rights('admin')
def index():
    return render_template('users/index.html', users=user_repository.all())

@bp.route('/<int:user_id>')
def show(user_id):
    user = user_repository.get_by_id(user_id)
    if user is None:
        flash('Пользователя нет в базе данных!', 'danger')
        return redirect(url_for('users.index'))
    user_role = role_repository.get_by_id(user.role_id)
    return render_template('users/show.html', user_data=user, user_role=getattr(user_role, 'name', ''))

@bp.route('/new', methods = ['POST', 'GET'])
@login_required
@check_rights('admin')
def new():
    user_data = {}
    if request.method == 'POST':
        fields = ('username', 'password', 'first_name', 'middle_name', 'last_name', 'role_id')
        user_data = { field: request.form.get(field) or None for field in fields }
        
        validation_error = 'Username должен содержать хотя бы 5 символов!' if (user_data['username'] is None or len(user_data['username']) < 5) else password_validator(user_data['password']) 
        
        if validation_error:
            flash(validation_error, 'danger')
            return render_template('users/new.html', user_data=user_data, roles=role_repository.all(), val_error=validation_error)
        
        try:
            user_repository.create(**user_data)
            flash('Учетная запись успешно создана', 'success')
            return redirect(url_for('users.index'))
        except connector.errors.DatabaseError:
            flash('Произошла ошибка при создании записи. Проверьте, что все необходимые поля заполнены', 'danger')
            db.connect().rollback()
    return render_template('users/new.html', user_data=user_data, roles=role_repository.all())

@bp.route('/<int:user_id>/delete', methods = ['POST'])
@login_required
@check_rights('admin')
def delete(user_id):
    user_repository.delete(user_id)
    flash('Учетная запись успено удалена', 'success')
    return redirect(url_for('users.index'))

@bp.route('/<int:user_id>/edit', methods = ['POST', 'GET'])
@login_required
@check_rights('admin')
def edit(user_id):
    user = user_repository.get_by_id(user_id)
    if user is None:
        flash('Пользователя нет в базе данных!', 'danger')
        return redirect(url_for('users.index'))
    
    if request.method == 'POST':
        fields = ('first_name', 'middle_name', 'last_name', 'role_id')
        user_data = { field: request.form.get(field) or None for field in fields }
        try:
            user_repository.update(user_id, **user_data)
            flash('Учетная запись успешно изменена', 'success')
            return redirect(url_for('users.index'))
        except connector.errors.DatabaseError:
            flash('Произошла ошибка при изменении записи.', 'danger')
            db.connect().rollback()
            user = user_data
    return render_template('users/edit.html', user_data=user, roles=role_repository.all())

@bp.route('/<int:user_id>/changepassword', methods = ['POST', 'GET'])
@login_required
def changepassword(user_id):
    user = user_repository.get_by_id(user_id)
    old_password_validation = None
    passwords_not_matching = None
    validation_error = None
    user_data = {}
    
    if user is None:
        flash('Пользователя нет в базе данных!', 'danger')
        return redirect(url_for('users.index'))
    
    if request.method == 'POST':
        fields = ('old_password', 'new_password', 'new_password_r')
        user_data = { field: request.form.get(field) or None for field in fields }
        
        # print(user[0])
        check = user_repository.validate_password(user[0], user_data['old_password'])
        
        if check is None:
            old_password_validation = "Неверный старый пароль!"
        
        if user_data['new_password'] != user_data['new_password_r']:
            passwords_not_matching = "Пароли не совпадают!"

        validation_error = password_validator(user_data['new_password'])
                    
        if not validation_error and not passwords_not_matching and not old_password_validation:
            try:
                user_repository.change_password(user[0], user_data["new_password"])
                flash('Пароль успешно изменен', 'success')
                return redirect(url_for('users.index'))
            except connector.errors.DatabaseError:
                flash('Произошла ошибка при изменении пароля.', 'danger')
                db.connect().rollback()
                
    # print(validation_error)
          
    return render_template('users/changepassword.html', validation_error=validation_error, old_password_validation=old_password_validation, passwords_not_matching=passwords_not_matching, user_data=user_data)