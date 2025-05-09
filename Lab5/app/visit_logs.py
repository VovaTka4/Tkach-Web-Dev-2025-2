import csv
from io import StringIO, BytesIO

from flask import Blueprint, render_template, request, send_file
from flask_login import login_required, current_user

from .repositories.visit_logs_repository import VisitLogsRepository
from .repositories.user_repository import UserRepository
from .db import db

bp = Blueprint('visit_logs', __name__, url_prefix='/visit_logs')

visit_log_repository = VisitLogsRepository(db)
user_repository = UserRepository(db)

@bp.route('/visits')
@login_required
def visits():
    page = int(request.args.get('page', 1))
    offset = (page - 1) * 20
    
    logs = visit_log_repository.paginated(offset)
    total = visit_log_repository.count()

    user_dict = {
        user.id: f"{user.last_name} {user.first_name} {user.middle_name or ''}".strip()
        for user in user_repository.all()
    }

    return render_template(
        'visit_logs/visits.html',
        visit_logs=logs,
        users=user_dict,
        current_page = page,
        total_pages = (total + 20 - 1) // 20
    )

@bp.route('/by_pages')
@login_required
def by_pages():
    stats = visit_log_repository.page_stats()
    return render_template('visit_logs/by_pages.html', page_stats=stats)

@bp.route('/by_users')
@login_required
def by_users():
    stats = visit_log_repository.user_stats()
    return render_template('visit_logs/by_users.html', user_stats=stats)

@bp.route('/export/users')
@login_required
def export_users_csv():
    stats = visit_log_repository.user_stats()
    
    output = BytesIO()
    output.write('\ufeff'.encode('utf-8'))
    
    text_stream = StringIO()
    writer = csv.writer(text_stream, delimiter=';')
    writer.writerow(['№', 'Пользователь', 'Количество посещений'])

    for i, row in enumerate(stats, 1):
        username = row.username if row.username else "Неаутентифицированный пользователь"
        writer.writerow([i, username, row.count])

    output.write(text_stream.getvalue().encode('utf-8'))
    output.seek(0)

    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name='users_report.csv'
    )
    
@bp.route('/export/pages')
@login_required
def export_pages_csv():
    stats = visit_log_repository.page_stats()
    
    output = BytesIO()
    output.write('\ufeff'.encode('utf-8'))
    
    text_stream = StringIO()
    writer = csv.writer(text_stream, delimiter=';')
    writer.writerow(['№', 'Страница', 'Количество посещений'])

    for i, row in enumerate(stats, 1):
        writer.writerow([i, row.path, row.count])

    output.write(text_stream.getvalue().encode('utf-8'))
    output.seek(0)

    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name='pages_report.csv'
    )