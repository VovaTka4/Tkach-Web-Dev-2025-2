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

bp = Blueprint('meals', __name__, url_prefix='/meals')

@bp.route('/')
def index():
    return render_template('meals/index.html')