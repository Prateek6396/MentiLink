from database import db
from datetime import datetime

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='In Progress') # "In Progress" or "Completed"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Goal {self.description[:30]}>'