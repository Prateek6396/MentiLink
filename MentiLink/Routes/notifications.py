from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models.notification import Notification
from database import db

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/')
@login_required
def index():
    # Fetch notifications and mark them all as read when the page is visited
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.timestamp.desc()).all()
    for notification in notifications:
        notification.is_read = True
    db.session.commit()

    return render_template('notifications.html', notifications=notifications)

@notifications_bp.route('/<int:notification_id>/go')
@login_required
def go_to_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id != current_user.id:
        return redirect(url_for('notifications.index'))

    notification.is_read = True
    db.session.commit()

    if notification.link:
        return redirect(notification.link)
    return redirect(url_for('notifications.index'))