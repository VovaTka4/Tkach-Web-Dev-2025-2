from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
import mysql.connector as connector
from .repositories.user_repository import UserRepository
from .repositories.m2m_product_meal_repository import M2MProductMealRepository
from .repositories.meal_repository import MealRepository
from .repositories.product_repository import ProductRepository
from .db import db

user_repository = UserRepository(db)
product_repository = ProductRepository(db)
meal_repository = MealRepository(db)
m2m_product_meal = M2MProductMealRepository(db)

bp = Blueprint('pages', __name__, url_prefix='/pages')

@bp.route('/bmr_calculator', methods=['GET', 'POST'])
@login_required
def bmr_calculator():
    result = None
    user_data = {}
    
    if request.method == 'POST':
        fields = ('age', 'height', 'weight', 'gender', 'activity', 'goal')
        user_data = { field: request.form.get(field) or None for field in fields }
        
        try:
            # Формула Харриса-Бенедикта
            if user_data['gender'] == 'male':
                bmr = (10 * int(user_data['weight'])) + (6.25 * int(user_data['height'])) - (5 * int(user_data['age'])) + 5
            else:
                bmr = (10 * int(user_data['weight'])) + (6.25 * int(user_data['height'])) - (5 * int(user_data['age'])) - 161

            calories = bmr * int(user_data['activity'])

            if user_data['goal'] == 'lose':
                calories -= 500
            elif user_data['goal'] == 'gain':
                calories += 500

            protein = round((calories * 0.3) / 4)
            fat = round((calories * 0.25) / 9)
            carbs = round((calories * 0.45) / 4)
            
            result = {
                      'calories': calories,
                      'protein': protein,
                      'fat': fat,
                      'carbs': carbs
                     }
            
            return render_template('pages/bmr_calculator.html', result=result)
        
        except connector.errors.DatabaseError:
            flash('Произошла ошибка при создании записи. Проверьте, что все необходимые поля заполнены', 'danger')
            db.connect().rollback()
            
    return render_template('pages/bmr_calculator.html', result=result)

@bp.route('/save_bmr', methods=['POST'])
@login_required
def save_bmr():
    try:
        calories = int(request.form['calories'])
        protein = int(request.form['protein'])
        fat = int(request.form['fat'])
        carbs = int(request.form['carbs'])
        goal = request.form.get('goal', 'maintain')

        user_repository.set_goal(current_user.get_id(), goal, calories, protein, fat, carbs)
        flash('Цели успешно сохранены!', 'success')
    except Exception as e:
        print("Ошибка при сохранении целей:", e)
        flash('Ошибка при сохранении целей. Попробуйте ещё раз.', 'danger')
        db.connect().rollback()
    
    return redirect(url_for('pages.bmr_calculator'))