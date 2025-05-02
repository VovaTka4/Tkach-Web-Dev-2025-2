from functools import wraps
from flask import redirect, url_for, flash, g
from flask_login import current_user

from ..repositories.role_repository import RoleRepository
from ..db import db

role_repository = RoleRepository(db)

def check_rights(required_permission):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):            
            user_role = role_repository.get_by_id(current_user.role_id).name
            g.has_permission = (user_role == required_permission)
            user_id = kwargs.get("user_id")
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" + dir(current_user))
            if (not g.has_permission) or (user_role != required_permission and current_user.id == user_id):
                flash("У вас недостаточно прав для данного действия.", "danger")
                return redirect(url_for("index"))
            return func(*args, **kwargs)
        return wrapper
    return decorator
