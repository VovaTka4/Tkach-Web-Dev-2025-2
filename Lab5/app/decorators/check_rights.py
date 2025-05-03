from functools import wraps
from flask import redirect, render_template, url_for, flash, g, request
from flask_login import current_user

from ..repositories.role_repository import RoleRepository
from ..repositories.user_repository import UserRepository
from ..db import db

role_repository = RoleRepository(db)
user_repository = UserRepository(db)

def has_rights(required_permission):
    if not current_user.is_authenticated:
        return False
    user = user_repository.get_by_id(current_user.id)
    if not user:
        return False
    role = role_repository.get_by_id(user.role_id)
    return role and role.name == required_permission

def check_rights(required_permission):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):   
                    
            user_id = kwargs.get('user_id')
            
            g.is_admin = has_rights(required_permission)
            g.has_rights =  (user_id == current_user.id)
            
            if g.has_rights or g.is_admin:
                return func(*args, **kwargs)
            
            flash('У вас недостаточно прав для доступа к данной странице! USERID:' + str(user_id) + " CURRENTUSERID: " + str(current_user.id), 'warning')
            return redirect(url_for('users.index'))
        
        return wrapper
    return decorator