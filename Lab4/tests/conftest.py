import os
from functools import reduce
from collections import namedtuple
import logging
import pytest
import mysql.connector
from app import create_app 
from app.db import DBConnector
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository


TEST_DB_CONFIG = {
    'MYSQL_USER': 'Tkach231329',
    'MYSQL_PASSWORD': 'PAmysql1488_52-42',
    'MYSQL_HOST': 'Tkach231329.mysql.pythonanywhere-services.com',
    'MYSQL_DATABASE': 'Tkach231329$lab4test',
}

def get_connection(app):
    return mysql.connector.connect(
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        host=app.config['MYSQL_HOST'],
        database=app.config['MYSQL_DATABASE']
    )
    
def setup_db(app):
    logging.getLogger().info("Dropping tables, creating new...")
    with app.open_resource('schema.sql') as f:
        schema_query = f.read().decode('utf8')
    connection = get_connection(app)
    query = '\n'.join([f"USE {app.config['MYSQL_DATABASE']};", schema_query])
    with connection.cursor(named_tuple = True) as cursor:
        for _ in cursor.execute(query, multi=True):
            pass
    connection.commit()
    connection.close()
    
def teardown_db(app):
    connection = get_connection(app)
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS roles;") 
    cursor.execute("DROP TABLE IF EXISTS users;")
    connection.commit()
    cursor.close()
    connection.close()
    
@pytest.fixture(scope='session')
def app():
    return create_app(TEST_DB_CONFIG)

@pytest.fixture(scope='session') #по умолчанию: для каждого теста отдельно и заново, scope=session - вся сессия тестов
def db_connector(app):
    setup_db(app)
    with app.app_context():
        connector = DBConnector(app)
        yield connector #фикстура - функция генератор, все что до yield - инициализация, yield - значенеи фикстуры, после - высвобождение ресурсов и тд
        connector.disconnect()
    teardown_db(app)
    
@pytest.fixture
def role_repository(db_connector):
    return RoleRepository(db_connector)

@pytest.fixture
def user_repository(db_connector):
    return UserRepository(db_connector)

@pytest.fixture
def existing_role(db_connector):
    #arrange, задача данных и запись в бд
    data = (1, 'admin')
    row_class = namedtuple('Row', ['id', 'name'])
    role = row_class(*data)
    
    connection = db_connector.connect()
    with connection.cursor() as cursor:
        query = 'INSERT INTO roles(id, name) VALUES (%s, %s);'
        cursor.execute(query, data)
        connection.commit()
        
    #возвращаем роль
    yield role
    
    #очищаем после теста
    with connection.cursor() as cursor:
        query = 'DELETE FROM roles WHERE id=%s;'
        cursor.execute(query, (role.id,))
        connection.commit()
        
@pytest.fixture
def nonexisting_role_id():
    return 1

@pytest.fixture
def example_roles(db_connector):
    #arrange, задача данных и запись в бд
    data = [(1, 'admin'), (2, 'test')]
    row_class = namedtuple('Row', ['id', 'name'])
    roles = [row_class(*row_data) for row_data in data]
    
    connection = db_connector.connect()
    with connection.cursor() as cursor:
        placeholders = ', '.join(['(%s, %s)' for _ in range(len(data))])
        query = f"INSERT INTO roles(id, name) VALUES {placeholders};"
        cursor.execute(query, reduce(lambda seq, x: seq + list(x), data, []))
        connection.commit()
        
    #возвращаем роль
    yield roles
    
    #clean up, очищаем после теста
    with connection.cursor() as cursor:
        roles_ids = ', '.join([str(role.id) for role in roles])
        query = f"DELETE FROM roles WHERE id IN ({roles_ids});"
        cursor.execute(query)
        connection.commit()
        
@pytest.fixture
def existing_user(db_connector):
    #arrange, задача данных и запись в бд
    data = (1, 'admin', 'adminFN', 'adminLN', 'qwerty', 1)
    row_class = namedtuple('Row', ['id', 'username', 'first_name', 'last_name', 'password_hash', 'role_id'])
    user = row_class(*data)
    
    connection = db_connector.connect()
    with connection.cursor() as cursor:
        query = 'INSERT INTO roles(id, name) VALUES (%s, %s);'
        cursor.execute(query, (1, 'admin'))
        query = 'INSERT INTO users(id, username, first_name, last_name, password_hash, role_id) VALUES (%s, %s, %s, %s, SHA2(%s, 256), %s);'
        cursor.execute(query, data)
        connection.commit()
        
    #возвращаем роль
    yield user
    
    #очищаем после теста
    with connection.cursor() as cursor:
        query = 'DELETE FROM roles WHERE id=%s;'
        cursor.execute(query, (1,))
        query = 'DELETE FROM users WHERE id=%s;'
        cursor.execute(query, (user.id,))
        connection.commit()
        
@pytest.fixture
def nonexisting_user_id():
    return 1

@pytest.fixture
def example_users(db_connector):
    #arrange, задача данных и запись в бд
    data = [(1, 'admin', 'adminFN', 'adminLN', 'qwerty', 1), (2, 'test', 'testFN', 'testLN', 'qwerty', 1)]
    row_class = namedtuple('Row', ['id', 'username', 'first_name', 'last_name', 'password_hash', 'role_id'])
    users = [row_class(*row_data) for row_data in data]
    
    connection = db_connector.connect()
    with connection.cursor() as cursor:
        query = 'INSERT INTO roles(id, name) VALUES (%s, %s);'
        cursor.execute(query, (1, 'admin'))
        placeholders = ', '.join(['(%s, %s, %s, %s, SHA2(%s, 256), %s)' for _ in range(len(data))])
        query = f"INSERT INTO users(id, username, first_name, last_name, password_hash, role_id) VALUES {placeholders};"
        cursor.execute(query, reduce(lambda seq, x: seq + list(x), data, []))
        connection.commit()
        
    #возвращаем роль
    yield users
    
    #clean up, очищаем после теста
    with connection.cursor() as cursor:
        query = 'DELETE FROM roles WHERE id=%s;'
        cursor.execute(query, (1,))
        users_ids = ', '.join([str(role.id) for role in users])
        query = f"DELETE FROM users WHERE id IN ({users_ids});"
        cursor.execute(query)
        connection.commit()
        
@pytest.fixture
def client(app):
    return app.test_client()

# для запуска: находимся в Lab4: python -m pytest -p no:warnings --log-cli-level=INFO
# ключи -p и --log-cli-level=INFO - не обязательно
# -p no:warnings <- не показывает лишние предупреждения всякие
# --log-cli-level=INFO <- информационные логи будут отображаться, чтоб посмотреть этапы инициализации и удаления базы, в какие моменты они происходят