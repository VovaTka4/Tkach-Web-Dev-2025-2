from werkzeug.middleware.dispatcher import DispatcherMiddleware
from Lab1.app.app import app as lab1_app
from Lab2.app.app import app as lab2_app
from Lab3.app.app import app as lab3_app
from Lab4.app import create_app as create_lab4_app
from Lab5.app import create_app as create_lab5_app


from root_app.app import app as root_app

lab4_app = create_lab4_app()
lab5_app = create_lab5_app()

app = DispatcherMiddleware(root_app, {
    '/lab1': lab1_app,
    '/lab2': lab2_app,
    '/lab3': lab3_app,
    '/lab4': lab4_app,
    '/lab5': lab5_app,
})

application = app