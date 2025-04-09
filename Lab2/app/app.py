import random
import re
from flask import Flask, render_template, abort, request, make_response

app = Flask(__name__)
application = app

def phone_validator(phone):
    
    phone_parsed = re.sub(r'[\- ().]','',phone)
    
    if phone_parsed.startswith(('+7')) and len(phone_parsed) == 12:
        phone_parsed = phone_parsed[2:]
    elif len(phone_parsed) == 11 and phone_parsed.startswith('8'):
        phone_parsed = phone_parsed[1:]
    elif len(phone_parsed) == 10:
        pass
    else:  
        return "", "Недопустимый ввод. Неверное количество цифр."
    
    if re.search(r'[^\d]', phone_parsed):
        return "", "Недопустимый ввод. В номере телефона встречаются недопустимые символы." 
    
    return f"8-{phone_parsed[:3]}-{phone_parsed[3:6]}-{phone_parsed[6:8]}-{phone_parsed[8:]}", ""
    

@app.route('/', methods=['GET', 'POST'])
def index():
    
    error = ""
    phone = ""
    
    if request.method == 'POST':
        phone = request.form['phone']
        
        phone, error = phone_validator(phone)
    
    return render_template('index.html', error=error, phone=phone, form = request.form)

@app.route('/cookies')
def cookies():
        
    cookie_value = request.cookies.get('MY_COOKIE')
    
    response = make_response(render_template('cookies.html', title='Cookie', cookies=request.cookies))
    
    if not cookie_value:
        response.set_cookie('MY_COOKIE', 'IS WORKING!', max_age=60 * 60 * 24 * 365)
    else:
        response.set_cookie('MY_COOKIE', '', max_age=0)
    
    return response

@app.route('/formparams', methods=['GET', 'POST'])
def formparams():
    if request.method == 'POST':
        return render_template('formparams.html', title='Параметры формы', form_data=request.form)
    return render_template('formparams.html', title='Параметры формы', form_data=None)

@app.route('/headers')
def headers():
    return render_template('headers.html', title='Заголовки запроса', headers=request.headers)

@app.route('/urlparams')
def urlparams():
    return render_template('urlparams.html', title='Параметры URL', urlparams = request.args)