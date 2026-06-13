from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from app.models.booking import Booking
from app.models.room import Room
from app import mysql
from functools import wraps

report_bp = Blueprint('report', __name__)

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@report_bp.route('/')
@admin_required
def index():
    cur = mysql.connection.cursor()

    # booking per status
    cur.execute("""
        SELECT status, COUNT(*) as count FROM bookings GROUP BY status
    """)
    status_stats = cur.fetchall()

    # most booked rooms
    cur.execute("""
        SELECT r.name, COUNT(b.id) as total
        FROM bookings b JOIN rooms r ON b.room_id = r.id
        WHERE b.status = 'approved'
        GROUP BY r.id ORDER BY total DESC LIMIT 5
    """)
    top_rooms = cur.fetchall()

    # bookings per month (current year)
    cur.execute("""
        SELECT MONTH(date) as month, COUNT(*) as total
        FROM bookings
        WHERE YEAR(date) = YEAR(CURDATE())
        GROUP BY MONTH(date) ORDER BY month
    """)
    monthly = cur.fetchall()

    cur.close()

    return render_template('admin/report.html',
        status_stats=status_stats,
        top_rooms=top_rooms,
        monthly=monthly
    )