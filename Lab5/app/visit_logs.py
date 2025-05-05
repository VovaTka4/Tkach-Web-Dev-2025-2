from flask import Blueprint, render_template, request, send_file
from flask_login import login_required, current_user
from io import StringIO
import csv

from .repositories.visit_logs_repository import VisitLogsRepository
from .repositories.user_repository import UserRepository
from .db import db

bp = Blueprint('visit_logs', __name__, url_prefix='/visit-logs')

visit_log_repository = VisitLogsRepository(db)
user_repository = UserRepository(db)

@bp.route('/visit_logs')
@login_required
def index():
    page = int(request.args.get('page', 1))
    per_page = 20
    offset = (page - 1) * per_page

    logs = visit_log_repository.paginated(per_page, offset)
    total = visit_log_repository.count()

    user_dict = {
        user.id: f"{user.last_name} {user.first_name} {user.middle_name or ''}".strip()
        for user in user_repository.all()
    }

    return render_template(
        'visit_logs/visits.html',
        visit_logs=logs,
        users=user_dict,
        current_page=page,
        total_pages=(total + per_page - 1) // per_page    
    )

@bp.route('/visit_logs/by_pages')
@login_required
def by_pages():
    stats = visit_log_repository.page_stats()
    return render_template('visit_logs/pages_report.html', page_stats=stats)

@bp.route('/visit_logs/by_users')
@login_required
def by_users():
    stats = visit_log_repository.user_stats()
    for row in stats:
        if row['user_id'] is None:
            row['username'] = "Неаутентифицированный пользователь"
        else:
            user = user_repository.get_by_id(row['user_id'])
            if user:
                row['username'] = f"{user.last_name or ''} {user.first_name or ''} {user.middle_name or ''}".strip()
            else:
                row['username'] = "—"
    return render_template('visit_logs/users_report.html', user_stats=stats)

@bp.route('/export/pages')
@login_required
def export_pages_csv():
    stats = visit_log_repository.page_stats()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['№', 'Страница', 'Количество посещений'])
    for i, row in enumerate(stats, 1):
        writer.writerow([i, row['path'], row['count']])
    output.seek(0)
    return send_file(output, mimetype='text/csv', as_attachment=True, download_name='pages_report.csv')

@bp.route('/export/users')
@login_required
def export_users_csv():
    stats = visit_log_repository.user_stats()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['№', 'Пользователь', 'Количество посещений'])
    for i, row in enumerate(stats, 1):
        if row['user_id'] is None:
            username = "Неаутентифицированный пользователь"
        else:
            user = user_repository.get_by_id(row['user_id'])
            username = f"{user.last_name or ''} {user.first_name or ''} {user.middle_name or ''}".strip() if user else "—"
        writer.writerow([i, username, row['count']])
    output.seek(0)
    return send_file(output, mimetype='text/csv', as_attachment=True, download_name='users_report.csv')
