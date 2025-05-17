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

bp = Blueprint('product', __name__, url_prefix='/product')

def inside(value, min_val, max_val):
    return (min_val is None or value >= min_val) and (max_val is None or value <= max_val)

@bp.route('/products', methods=['GET'])
@login_required
def products():
    try:
        name = request.args.get('name')
        mine = request.args.get('mine') == 'on'
        shared = request.args.get('shared') == 'on'

        filters = {
            'calories_min': request.args.get('calories_min', default=0, type=int),
            'calories_max': request.args.get('calories_max', default=1000000, type=int),
            'protein_min': request.args.get('protein_min', default=0, type=int),
            'protein_max': request.args.get('protein_max', default=1000000, type=int),
            'fat_min': request.args.get('fat_min', default=0, type=int),
            'fat_max': request.args.get('fat_max', default=1000000, type=int),
            'carbs_min': request.args.get('carbs_min', default=0, type=int),
            'carbs_max': request.args.get('carbs_max', default=1000000, type=int),
        }

        all_products = product_repository.all()

        filtered = []
        for p in all_products:
            if p.owner_id != current_user.get_id() and not p.is_public:
                continue
            if name and name.lower() not in p.product_name.lower():
                continue
            if mine and p.owner_id != current_user.get_id():
                continue
            if not shared and p.is_public:
                continue
            if not mine and not p.is_public:
                continue

            if not inside(p.kalories, filters['calories_min'], filters['calories_max']):
                continue
            if not inside(p.protein, filters['protein_min'], filters['protein_max']):
                continue
            if not inside(p.fat, filters['fat_min'], filters['fat_max']):
                continue
            if not inside(p.carbohydrates, filters['carbs_min'], filters['carbs_max']):
                continue

            filtered.append(p)

        return render_template('product/products.html', products=filtered)
    
    except connector.errors.DatabaseError as e:
        flash('Ошибка при получении списка продуктов.', 'danger')
        print(e)
        return render_template('products/product.html', products=[])
    
@bp.route('/new', methods=['GET', 'POST'])
@login_required
def create_product():
    if request.method == 'POST':
        name = request.form['name']
        calories = request.form['calories']
        protein = request.form['protein']
        fat = request.form['fat']
        carbs = request.form['carbs']
        image = request.files.get('image')
        img_path = 'static/placeholder.png'  # Заглушка

        product_repository.create(name, calories, protein, fat, carbs, img_path, False, current_user.get_id())
        flash('Продукт создан', 'success')
        return redirect(url_for('product.products'))

    return render_template('product/new.html')


@bp.route('/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
@check_rights('edit_product')
def edit_product(product_id):
    product = product_repository.get_by_id(product_id)
    if not product:
        flash('Продукт не найден', 'danger')
        return redirect(url_for('products.product'))

    if request.method == 'POST':
        name = request.form['name']
        calories = request.form['calories']
        protein = request.form['protein']
        fat = request.form['fat']
        carbs = request.form['carbs']
        image = request.files.get('image')
        img_path = product.img_path or 'img/placeholder.png'

        product_repository.update(product_id, name, calories, protein, fat, carbs, img_path)
        flash('Продукт обновлен', 'success')
        return redirect(url_for('product.products'))

    return render_template('product/edit.html', product=product)
