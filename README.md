UNIQUE MEAL Member Management System in Python, let's dive into a more detailed implementation. We will use Flask (a Python web framework) along with SQLite for database management. The system will include features like:

Member Registration and Login
Meal/Event Booking
Profile Management
Admin Dashboard
Payment Processing (optional)
Step-by-Step Code Implementation
1. Project Setup
First, you need to install the required libraries:

bash
Copy code
pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF
2. Directory Structure
csharp
Copy code
unique_meal/
├── app.py                # Main application file
├── models.py             # Database models
├── forms.py              # Forms for registration, login, etc.
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── profile.html
└── static/               # Static files (CSS, JS)
3. Create app.py (Main Flask App)
python
Copy code
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///members.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Member model
class Member(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    membership_tier = db.Column(db.String(50), nullable=False, default='Basic')

@login_manager.user_loader
def load_user(member_id):
    return Member.query.get(int(member_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='sha256')
        new_member = Member(username=username, email=email, password=hashed_password)
        db.session.add(new_member)
        db.session.commit()
        login_user(new_member)
        return redirect(url_for('profile'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        member = Member.query.filter_by(email=email).first()
        if member and check_password_hash(member.password, password):
            login_user(member)
            return redirect(url_for('profile'))
        else:
            flash('Login Unsuccessful. Check email and password.')
    return render_template('login.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
4. Create models.py (Database Models)
In this file, you can define other models as your project grows (such as a model for managing meal bookings).

python
Copy code
from app import db

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    membership_tier = db.Column(db.String(50), nullable=False)

class MealBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    meal_name = db.Column(db.String(100), nullable=False)
    meal_date = db.Column(db.Date, nullable=False)
    booked_on = db.Column(db.DateTime, default=datetime.utcnow)
5. Create forms.py (Form Handling)
For better form validation and handling, use Flask-WTF. Here’s an example of the registration form:

python
Copy code
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=100)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')
6. HTML Templates
Here’s a sample template for the registration page (register.html):

html
Copy code
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register</title>
</head>
<body>
    <h1>Register for UNIQUE MEAL</h1>
    <form method="POST">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username">
        <label for="email">Email:</label>
        <input type="email" id="email" name="email">
        <label for="password">Password:</label>
        <input type="password" id="password" name="password">
        <label for="confirm_password">Confirm Password:</label>
        <input type="password" id="confirm_password" name="confirm_password">
        <button type="submit">Register</button>
    </form>
</body>
</html>
7. Expanding with Features
Meal/Event Booking
You can create a separate form to allow users to book meals or events, which would be linked to their member profile. For instance, creating a route for booking:

python
Copy code
@app.route('/book_meal', methods=['GET', 'POST'])
@login_required
def book_meal():
    if request.method == 'POST':
        meal_name = request.form.get('meal_name')
        meal_date = request.form.get('meal_date')
        new_booking = MealBooking(member_id=current_user.id, meal_name=meal_name, meal_date=meal_date)
        db.session.add(new_booking)
        db.session.commit()
        flash('Meal booked successfully!')
    return render_template('book_meal.html')
8. Admin Dashboard
For admins, you can create separate routes that display all members and allow the admin to manage membership tiers, view bookings, etc.

This implementation can be expanded with other features like payment integration, reports, and email notifications as required by the system. Let me know if you'd like specific sections in more detail!
To implement an Admin Dashboard for your UNIQUE MEAL Member Management System in Python using Flask, you’ll need to add routes and templates specifically for administrators. The admin dashboard will allow administrators to manage members, view meal bookings, and possibly modify membership tiers or generate reports.

Here's how you can build it step by step:

Key Features for Admin Dashboard:
Admin Authentication: Only administrators should access this dashboard.
View Members: List all registered members.
Manage Memberships: Ability to change membership tiers.
View Meal Bookings: Display all bookings.
Reports: Generate basic reports on membership statistics or bookings.
Step-by-Step Code Implementation
1. Add an Admin Role to Member Model
First, modify your Member model to include an is_admin field that will distinguish regular users from admins.

python
Copy code
# models.py
class Member(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    membership_tier = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Add this field for admin roles
Now, we can assign some users as admins by setting is_admin=True when creating their accounts or through the database manually.

2. Create Admin-Only Routes
Add specific routes that can only be accessed by users who have the is_admin flag set to True.

python
Copy code
# app.py
from flask import abort

def admin_required(func):
    """Decorator to ensure only admins can access certain routes."""
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)  # Forbidden access
        return func(*args, **kwargs)
    return wrapper

@app.route('/admin')
@admin_required
def admin_dashboard():
    members = Member.query.all()
    return render_template('admin/dashboard.html', members=members)

@app.route('/admin/members')
@admin_required
def manage_members():
    members = Member.query.all()  # Fetch all members
    return render_template('admin/manage_members.html', members=members)

@app.route('/admin/bookings')
@admin_required
def view_bookings():
    bookings = MealBooking.query.all()  # Fetch all bookings
    return render_template('admin/view_bookings.html', bookings=bookings)
The @admin_required decorator ensures that only users who are admins can access these routes.

3. Create HTML Templates for the Admin Dashboard
Base Admin Template (admin_base.html): This template will serve as the layout for all admin-related pages.

html
Copy code
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <h1>Admin Dashboard</h1>
    <nav>
        <a href="{{ url_for('admin_dashboard') }}">Dashboard</a> |
        <a href="{{ url_for('manage_members') }}">Manage Members</a> |
        <a href="{{ url_for('view_bookings') }}">View Bookings</a> |
        <a href="{{ url_for('logout') }}">Logout</a>
    </nav>
    <div class="content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
Admin Dashboard (dashboard.html): The main page of the admin dashboard where an admin can see an overview of members and bookings.

html
Copy code
{% extends "admin/admin_base.html" %}
{% block content %}
<h2>Welcome, Admin!</h2>
<p>Here are some quick stats:</p>
<ul>
    <li>Total Members: {{ members|length }}</li>
    <!-- You can add more stats like number of bookings, events, etc. -->
</ul>
{% endblock %}
Manage Members Page (manage_members.html): This page lists all members and allows the admin to change their membership tiers.

html
Copy code
{% extends "admin/admin_base.html" %}
{% block content %}
<h2>Manage Members</h2>
<table>
    <thead>
        <tr>
            <th>Username</th>
            <th>Email</th>
            <th>Membership Tier</th>
            <th>Admin</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for member in members %}
        <tr>
            <td>{{ member.username }}</td>
            <td>{{ member.email }}</td>
            <td>{{ member.membership_tier }}</td>
            <td>{{ 'Yes' if member.is_admin else 'No' }}</td>
            <td>
                <a href="{{ url_for('edit_member', member_id=member.id) }}">Edit</a>
                <!-- Add option to delete if needed -->
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
View Bookings Page (view_bookings.html): This page shows all meal bookings made by the members.

html
Copy code
{% extends "admin/admin_base.html" %}
{% block content %}
<h2>Meal Bookings</h2>
<table>
    <thead>
        <tr>
            <th>Member</th>
            <th>Meal</th>
            <th>Date</th>
            <th>Booked On</th>
        </tr>
    </thead>
    <tbody>
        {% for booking in bookings %}
        <tr>
            <td>{{ booking.member.username }}</td>
            <td>{{ booking.meal_name }}</td>
            <td>{{ booking.meal_date }}</td>
            <td>{{ booking.booked_on }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
4. Edit Member Feature
In your manage_members.html, there’s an option to edit members. To implement this, you can create a route that allows admins to edit membership tiers or make a user an admin.

python
Copy code
@app.route('/admin/edit_member/<int:member_id>', methods=['GET', 'POST'])
@admin_required
def edit_member(member_id):
    member = Member.query.get_or_404(member_id)
    if request.method == 'POST':
        member.membership_tier = request.form.get('membership_tier')
        member.is_admin = bool(request.form.get('is_admin'))
        db.session.commit()
        flash('Member updated successfully!')
        return redirect(url_for('manage_members'))
    return render_template('admin/edit_member.html', member=member)
Edit Member Template (edit_member.html):

html
Copy code
{% extends "admin/admin_base.html" %}
{% block content %}
<h2>Edit Member - {{ member.username }}</h2>
<form method="POST">
    <label for="membership_tier">Membership Tier:</label>
    <input type="text" id="membership_tier" name="membership_tier" value="{{ member.membership_tier }}">

    <label for="is_admin">Admin:</label>
    <input type="checkbox" id="is_admin" name="is_admin" {% if member.is_admin %} checked {% endif %}>

    <button type="submit">Save Changes</button>
</form>
{% endblock %}
5. Authorization and Security
Admin Access Only: The admin_required decorator ensures that only admins can access the admin panel.
Flask-Login: Make sure that all admin routes are protected with @login_required so unauthorized users cannot access these routes.
6. Add CSS for Dashboard (Optional)
You can style your admin dashboard using a CSS file in your static/ directory to give it a professional look.
