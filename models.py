from app import db

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    membership_tier = db.Column(db.String(50), nullable=False)

# Run this once to create the database
db.create_all()
