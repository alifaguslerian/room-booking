# RoomBook

A web-based room booking system with role-based access (admin & user), built with Flask, MySQL, and vanilla JS.

## Tech Stack

- **Backend:** Python / Flask
- **Database:** MySQL
- **Frontend:** HTML, CSS (vanilla), JavaScript (vanilla)
- **Auth:** Flask-Login + Werkzeug password hashing

## Features

- Multi-role auth (admin / user)
- Admin: manage rooms (add, edit, delete), approve/reject bookings, view reports
- User: search rooms, submit bookings, cancel pending bookings
- Booking conflict detection
- Statistics dashboard & report page

## Setup

### Prerequisites

- Python 3.10+
- MySQL 8.0+ running on port 3306 (or configure custom port in `.env`)

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/room-booking.git
cd room-booking

python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
```

### Database

```bash
mysql -u root -p < schema.sql
```

### Environment

Create a `.env` file in the root directory:

```env
SECRET_KEY=your_random_secret_key
MYSQL_HOST=127.0.0.1
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=room_booking
MYSQL_PORT=3306
```

### Run

```bash
python run.py
```

Open `http://localhost:5000`

## Default Admin Account

username: admin
password: admin123

> Change the admin password after first login in production.

## Project Structure
room-booking/

├── app/

│   ├── models/        # OOP data models (User, Room, Booking)

│   ├── routes/        # Blueprint routes (auth, admin, user, report)

│   ├── static/        # CSS, JS

│   └── templates/     # Jinja2 HTML templates

├── schema.sql         # Database schema

├── run.py

└── requirements.txt