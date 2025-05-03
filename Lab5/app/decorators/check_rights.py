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
            
            g.has_permission = False
            
            if current_user.is_authenticated:
                user = user_repository.get_by_id(current_user.id)
                if user:
                    user_role = role_repository.get_by_id(user.role_id)
                    g.has_permission = (user_role.name == required_permission)
            
            if not g.has_permission:
                return redirect(url_for('users.index'))

            return func(*args, **kwargs)
        return wrapper
    return decorator
