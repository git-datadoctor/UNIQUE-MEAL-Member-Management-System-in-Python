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
