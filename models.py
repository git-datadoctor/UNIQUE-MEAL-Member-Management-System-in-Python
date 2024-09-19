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
