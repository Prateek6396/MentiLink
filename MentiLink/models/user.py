from database import db
from flask_login import UserMixin
from datetime import datetime
from models.session import Session

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'mentor' or 'student'
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    expertise = db.Column(db.Text)  # For mentors
    bio = db.Column(db.Text)
    qualification = db.Column(db.String(100)) 
    field_of_study = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    goals = db.relationship('Goal', backref='user', lazy=True, cascade="all, delete-orphan")


    @property
    def average_rating(self):
        if self.role != 'mentor':
            return None
        
        # Query for completed sessions with a rating
        ratings = db.session.query(db.func.avg(Session.rating)).filter(
            Session.mentor_id == self.id,
            Session.status == 'completed',
            Session.rating.isnot(None)
        ).scalar()

        return round(ratings, 1) if ratings else 0
    
    # Relationships
    mentor_sessions = db.relationship('Session', foreign_keys='Session.mentor_id', backref='mentor')
    student_sessions = db.relationship('Session', foreign_keys='Session.student_id', backref='student')
    slots = db.relationship('Slot', backref='mentor_user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'
