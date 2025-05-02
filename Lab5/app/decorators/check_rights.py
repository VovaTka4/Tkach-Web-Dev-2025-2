from functools import wraps
from flask import redirect, render_template, url_for, flash, g, request
from flask_login import current_user

from ..repositories.role_repository import RoleRepository
from ..repositories.user_repository import UserRepository
from ..db import db

role_repository = RoleRepository(db)
user_repository = UserRepository(db)

def check_rights(required_permission):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):   
            
            if not current_user.is_authenticated:
                flash("Пожалуйста, войдите в систему.", "danger")
                next_url = request.args.get('next', url_for('auth.login'))
                return redirect(next_url)
              
            user = user_repository.get_by_id(current_user.id) 
            user_role = role_repository.get_by_id(user.role_id).name
            g.has_permission = (user_role == required_permission)
            user_id = kwargs.get("user_id")
            if (not g.has_permission) or (user_role != required_permission and current_user.id == user_id):
                flash("У вас недостаточно прав для данного действия.", "danger")
                next_url = request.args.get('next', url_for('users.index'))
                return redirect(next_url)
            return func(*args, **kwargs)
        return wrapper
    return decorator
