from werkzeug.middleware.dispatcher import DispatcherMiddleware
from Lab1.app.app import app as lab1_app
from Lab2.app.app import app as lab2_app
from root_app.app import app as root_app

app = DispatcherMiddleware(root_app, {
    '/lab1': lab1_app,
    '/lab2': lab2_app
})

application = app