from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.user import User
from models.message import Message
from models.session import Session
from models.notification import Notification
from database import db
from sqlalchemy import or_, and_
from datetime import datetime
from pytz import timezone

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/conversation/<int:recipient_id>', methods=['GET', 'POST'])
@login_required
def conversation(recipient_id):
    recipient = User.query.get_or_404(recipient_id)
    
    # Security check: Ensure users can only message someone they have a session with
    session_exists = Session.query.filter(
        or_(
            and_(Session.mentor_id == current_user.id, Session.student_id == recipient_id),
            and_(Session.mentor_id == recipient_id, Session.student_id == current_user.id)
        )
    ).first()

    if not session_exists:
        flash("You can only message users with whom you have a session.", "danger")
        return redirect(url_for('dashboard.dashboard'))
        
    if request.method == 'POST':
        body = request.form.get('body')
        if body:
            # Create the message
            msg = Message(sender_id=current_user.id, recipient_id=recipient_id, body=body)
            db.session.add(msg)
            
            # Create the notification for the recipient
            notification = Notification(
                user_id=recipient_id,
                message=f"You have a new message from {current_user.full_name}.",
                link=url_for('messages.conversation', recipient_id=current_user.id)
            )
            db.session.add(notification)
            
            db.session.commit()
            return redirect(url_for('messages.conversation', recipient_id=recipient_id))

    messages = Message.query.filter(
        or_(
            and_(Message.sender_id == current_user.id, Message.recipient_id == recipient_id),
            and_(Message.sender_id == recipient_id, Message.recipient_id == current_user.id)
        )
    ).order_by(Message.timestamp.asc()).all()

    return render_template(
        'conversation.html', 
        messages=messages, 
        recipient=recipient,
        timezone=timezone  # Pass the timezone object
    )