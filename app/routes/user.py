from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from datetime import date
from app.models.room import Room
from app.models.booking import Booking

user_bp = Blueprint("user", __name__)


@user_bp.route("/dashboard")
@login_required
def dashboard():
    bookings = Booking.get_by_user(current_user.id)
    stats = {
        "total": len(bookings),
        "pending": sum(1 for b in bookings if b.status == "pending"),
        "approved": sum(1 for b in bookings if b.status == "approved"),
    }
    return render_template("user/dashboard.html", bookings=bookings[:5], stats=stats)


@user_bp.route("/search")
@login_required
def search():
    keyword = request.args.get("q", "")
    min_capacity = request.args.get("capacity", 0, type=int)
    rooms = Room.search(keyword, min_capacity)
    return render_template(
        "user/search.html", rooms=rooms, keyword=keyword, min_capacity=min_capacity
    )


@user_bp.route("/book/<int:room_id>", methods=["GET", "POST"])
@login_required
def book(room_id):
    room = Room.get_by_id(room_id)
    if not room or room.status == "maintenance":
        flash("Room not available.", "error")
        return redirect(url_for("user.search"))

    if request.method == "POST":
        booking_date = request.form.get("date")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        title = request.form.get("title")
        notes = request.form.get("notes", "")


        if start_time >= end_time:
            flash("End time must be after start time.", "error")
            return render_template("user/book.html", room=room, now=date.today())

        try:
            conflict = Booking.has_conflict(room_id, booking_date, start_time, end_time)
            if conflict:
                flash("Room already booked for that time slot.", "error")
                return render_template("user/book.html", room=room, now=date.today())
            Booking.create(
                current_user.id,
                room_id,
                title,
                booking_date,
                start_time,
                end_time,
                notes,
            )
            flash("Booking submitted, waiting for approval.", "success")
            return redirect(url_for("user.my_bookings"))
        except Exception as e:
            flash(f"Error: {str(e)}", "error")
            return render_template("user/book.html", room=room, now=date.today())

    return render_template("user/book.html", room=room, now=date.today())


@user_bp.route("/my-bookings")
@login_required
def my_bookings():
    bookings = Booking.get_by_user(current_user.id)
    return render_template("user/my_bookings.html", bookings=bookings)


@user_bp.route("/cancel/<int:booking_id>", methods=["POST"])
@login_required
def cancel_booking(booking_id):
    bookings = Booking.get_by_user(current_user.id)
    match = next((b for b in bookings if b.id == booking_id), None)
    if not match:
        flash("Booking not found.", "error")
        return redirect(url_for("user.my_bookings"))
    if match.status not in ("pending",):
        flash("Only pending bookings can be cancelled.", "error")
        return redirect(url_for("user.my_bookings"))
    Booking.update_status(booking_id, "cancelled")
    flash("Booking cancelled.", "success")
    return redirect(url_for("user.my_bookings"))
