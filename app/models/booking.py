from app import mysql
import datetime


def _td_to_str(td):
    if td is None:
        return "00:00"
    if isinstance(td, str):
        return td
    if isinstance(td, datetime.timedelta):
        total = int(td.total_seconds())
        h = total // 3600
        m = (total % 3600) // 60
        return f"{h:02d}:{m:02d}"
    return str(td)


class Booking:
    def __init__(self, id, user_id, room_id, title, date, start_time, end_time,
                 status, notes, created_at, **kwargs):
        self.id = id
        self.user_id = user_id
        self.room_id = room_id
        self.title = title
        self.date = date
        self.start_time = _td_to_str(start_time)
        self.end_time = _td_to_str(end_time)
        self.status = status
        self.notes = notes
        self.created_at = created_at
        for k, v in kwargs.items():
            setattr(self, k, v)

    @staticmethod
    def get_all():
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT b.*, u.username, r.name as room_name
            FROM bookings b
            JOIN users u ON b.user_id = u.id
            JOIN rooms r ON b.room_id = r.id
            ORDER BY b.created_at DESC
        """)
        rows = cur.fetchall()
        cur.close()
        return [Booking(**r) for r in rows]

    @staticmethod
    def get_by_user(user_id):
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT b.*, r.name as room_name, r.location
            FROM bookings b
            JOIN rooms r ON b.room_id = r.id
            WHERE b.user_id = %s
            ORDER BY b.date DESC
        """, (user_id,))
        rows = cur.fetchall()
        cur.close()
        return [Booking(**r) for r in rows]

    @staticmethod
    def create(user_id, room_id, title, date, start_time, end_time, notes=''):
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO bookings (user_id, room_id, title, date, start_time, end_time, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (user_id, room_id, title, date, start_time, end_time, notes))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def update_status(booking_id, status):
        cur = mysql.connection.cursor()
        cur.execute("UPDATE bookings SET status=%s WHERE id=%s", (status, booking_id))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def delete(booking_id):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def has_conflict(room_id, date, start_time, end_time, exclude_id=None):
        cur = mysql.connection.cursor()
        query = """
            SELECT id FROM bookings
            WHERE room_id = %s AND date = %s AND status != 'cancelled'
            AND start_time < %s AND end_time > %s
        """
        params = [room_id, date, end_time, start_time]
        if exclude_id:
            query += " AND id != %s"
            params.append(exclude_id)
        cur.execute(query, params)
        result = cur.fetchone()
        cur.close()
        return result is not None