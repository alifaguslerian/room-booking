from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import mysql, login_manager

class User(UserMixin):
    def __init__(self, id, username, email, password_hash, role, created_at):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.created_at = created_at

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_id(user_id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        row = cur.fetchone()
        cur.close()
        if not row:
            return None
        return User(**row)

    @staticmethod
    def get_by_username(username):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        row = cur.fetchone()
        cur.close()
        if not row:
            return None
        return User(**row)

    @staticmethod
    def create(username, email, password, role='user'):
        password_hash = generate_password_hash(password)
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)",
            (username, email, password_hash, role)
        )
        mysql.connection.commit()
        cur.close()

    def is_admin(self):
        return self.role == 'admin'


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))