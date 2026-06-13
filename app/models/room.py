from app import mysql

class Room:
    def __init__(self, id, name, location, capacity, facilities, status, created_at):
        self.id = id
        self.name = name
        self.location = location
        self.capacity = capacity
        self.facilities = facilities
        self.status = status
        self.created_at = created_at

    @staticmethod
    def get_all():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM rooms ORDER BY created_at DESC")
        rows = cur.fetchall()
        cur.close()
        return [Room(**r) for r in rows]

    @staticmethod
    def get_by_id(room_id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM rooms WHERE id = %s", (room_id,))
        row = cur.fetchone()
        cur.close()
        return Room(**row) if row else None

    @staticmethod
    def search(keyword='', min_capacity=0):
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT * FROM rooms
            WHERE (name LIKE %s OR location LIKE %s OR facilities LIKE %s)
            AND capacity >= %s
            AND status = 'available'
            ORDER BY name
        """, (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', min_capacity))
        rows = cur.fetchall()
        cur.close()
        return [Room(**r) for r in rows]

    @staticmethod
    def create(name, location, capacity, facilities):
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO rooms (name, location, capacity, facilities) VALUES (%s, %s, %s, %s)",
            (name, location, capacity, facilities)
        )
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def update(room_id, name, location, capacity, facilities, status):
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE rooms SET name=%s, location=%s, capacity=%s, facilities=%s, status=%s
            WHERE id=%s
        """, (name, location, capacity, facilities, status, room_id))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def delete(room_id):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM rooms WHERE id = %s", (room_id,))
        mysql.connection.commit()
        cur.close()