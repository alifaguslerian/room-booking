from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models.room import Room
from app.models.booking import Booking
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

# Dashboard
@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    bookings = Booking.get_all()
    rooms = Room.get_all()
    stats = {
        'total_rooms': len(rooms),
        'total_bookings': len(bookings),
        'pending': sum(1 for b in bookings if b.status == 'pending'),
        'approved': sum(1 for b in bookings if b.status == 'approved'),
    }
    return render_template('admin/dashboard.html', stats=stats, bookings=bookings[:10])

# Rooms
@admin_bp.route('/rooms')
@admin_required
def rooms():
    all_rooms = Room.get_all()
    return render_template('admin/rooms.html', rooms=all_rooms)

@admin_bp.route('/rooms/add', methods=['POST'])
@admin_required
def add_room():
    Room.create(
        request.form.get('name'),
        request.form.get('location'),
        request.form.get('capacity'),
        request.form.get('facilities')
    )
    flash('Room added.', 'success')
    return redirect(url_for('admin.rooms'))

@admin_bp.route('/rooms/edit/<int:room_id>', methods=['POST'])
@admin_required
def edit_room(room_id):
    Room.update(
        room_id,
        request.form.get('name'),
        request.form.get('location'),
        request.form.get('capacity'),
        request.form.get('facilities'),
        request.form.get('status')
    )
    flash('Room updated.', 'success')
    return redirect(url_for('admin.rooms'))

@admin_bp.route('/rooms/delete/<int:room_id>', methods=['POST'])
@admin_required
def delete_room(room_id):
    Room.delete(room_id)
    flash('Room deleted.', 'success')
    return redirect(url_for('admin.rooms'))

# Bookings
@admin_bp.route('/bookings')
@admin_required
def bookings():
    all_bookings = Booking.get_all()
    return render_template('admin/bookings.html', bookings=all_bookings)

@admin_bp.route('/bookings/<int:booking_id>/status', methods=['POST'])
@admin_required
def update_booking_status(booking_id):
    status = request.form.get('status')
    if status in ('approved', 'rejected'):
        Booking.update_status(booking_id, status)
        flash(f'Booking {status}.', 'success')
    return redirect(url_for('admin.bookings'))

@admin_bp.route('/bookings/delete/<int:booking_id>', methods=['POST'])
@admin_required
def delete_booking(booking_id):
    Booking.delete(booking_id)
    flash('Booking deleted.', 'success')
    return redirect(url_for('admin.bookings'))