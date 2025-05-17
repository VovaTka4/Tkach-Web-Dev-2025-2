from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
import mysql.connector as connector

from .repositories.user_repository import UserRepository
from .db import db

user_repository = UserRepository(db)

bp = Blueprint('meals', __name__, url_prefix='/meals')

@bp.route('/')
def index():
    return render_template('meals/index.html')