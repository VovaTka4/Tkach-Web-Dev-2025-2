import os

from flask import Flask, session, request
from flask_login import current_user
from .repositories.visit_logs_repository import VisitLogsRepository
from .db import db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile('config.py', silent=False)
    
    if test_config:
        app.config.from_mapping(test_config)
        
    db.init_app(app)
    
    visit_log_repository = VisitLogsRepository(db)
    
    from .cli import init_db_command
    app.cli.add_command(init_db_command)
    
    from . import auth
    app.register_blueprint(auth.bp)
    auth.login_manager.init_app(app)
    
    from . import users
    app.register_blueprint(users.bp)
    app.route('/', endpoint='index')(users.index)
            
    @app.before_request
    def log_visit():
        if request.endpoint and not request.endpoint.startswith('static'):
            path = request.path
            user_id = current_user.get_id() if current_user.is_authenticated else None
            try:
                visit_log_repository.create(path, user_id)
            except Exception as e:
                app.logger.warning(f'Не удалось сохранить лог посещения: {e}')
    
    return app