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
    
    from . import meals
    app.register_blueprint(meals.bp)
    app.route('/', endpoint='index')(meals.index)
    
    from . import pages
    app.register_blueprint(pages.bp)
    
    from . import product
    app.register_blueprint(product.bp)
    
    return app