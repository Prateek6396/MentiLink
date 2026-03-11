from database import db
from datetime import datetime
from pytz import timezone

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    slot_id = db.Column(db.Integer, db.ForeignKey('slot.id'), nullable=False)
    meeting_link = db.Column(db.String(200))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled
    summary = db.Column(db.Text)
    feedback = db.Column(db.Text)
    rating = db.Column(db.Integer)  # 1-5 rating
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    @property
    def is_active(self):
        """Checks if the current time is within the session's scheduled duration."""
        IST = timezone('Asia/Kolkata')
        now_in_ist = datetime.now(IST)
        
        slot_start_time_ist = IST.localize(self.slot.start_time)
        slot_end_time_ist = IST.localize(self.slot.end_time)
        
        return slot_start_time_ist <= now_in_ist <= slot_end_time_ist


    @property
    def is_past(self):
        """Checks if the session's end time has passed in IST."""
        IST = timezone('Asia/Kolkata')
        
        # Get the current time in IST
        now_in_ist = datetime.now(IST)
        
        # Take the naive time from the database and make it aware of IST
        slot_end_time_ist = IST.localize(self.slot.end_time)
        
        # Perform a correct, timezone-aware comparison
        return now_in_ist > slot_end_time_ist

    
    def __repr__(self):
        return f'<Session {self.title}>'
