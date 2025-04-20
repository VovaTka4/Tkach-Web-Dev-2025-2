# установить соединение 1 раз и дальше пользоваться при запросах к базе
# обьект соединения в Flask - обьект g, словарь, хранящий какие-то данные
from flask import g
import mysql.connector

class DBConnector:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
            
    def init_app(self, app):
        self.app = app
        self.app.teardown_appcontext(self.disconnect)
        # тут как раз метод об отключении
    
    # из приложения из инитапп получаем словарь с данными
    def _get_config(self):
        return {
            'user': self.app.config['MYSQL_USER'],
            'password': self.app.config["MYSQL_PASSWORD"],
            'host': self.app.config["MYSQL_HOST"],
            'database': self.app.config["MYSQL_DATABASE"]
        }
    
    # сохраняем ключ, если его нет, то создаем иначе возвращаем существующие (так получается одно и то же соединение всегда)
    def connect(self):
        if 'db' not in g:
            g.db = mysql.connector.connect(**self._get_config())
        return g.db
    
    # надо чтобы метод вызывался после обработки очередного запроса, что достигается с помощью строки13
    def disconnect(self, e=None):
        if 'db' in g:
            g.db.close
        g.pop('db', None)