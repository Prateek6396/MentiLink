from flask import Flask, render_template, redirect, url_for
from database import db
from flask_login import LoginManager, current_user
import os
from extensions import mail
from flask_mail import Mail, Message
from flask_login import current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('MENTILINK_SECRET', 'change-me-in-prod')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mentilink.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Use environment variables in production
app.config['MAIL_PASSWORD'] = 'your-app-password'   # Use environment variables in production
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'
app.config['MAIL_SUPPRESS_SEND'] = True # Set to False in production

mail = Mail(app)

db.init_app(app)
mail.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

# register blueprints
from Routes.auth import auth_bp
from Routes.dashboard import dashboard_bp
from Routes.sessions import sessions_bp
from Routes.mentors import mentors_bp
from Routes.messages import messages_bp
from Routes.notifications import notifications_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(sessions_bp, url_prefix='/sessions')
app.register_blueprint(mentors_bp, url_prefix='/mentors')
app.register_blueprint(messages_bp, url_prefix='/messages')
app.register_blueprint(notifications_bp, url_prefix='/notifications')

# import models so tables are known
import models.user
import models.session
import models.slot
from models.message import Message
from models.notification import Notification
from models.goal import Goal

@login_manager.user_loader
def load_user(user_id):
    from models.user import User
    return db.session.get(User, int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    return render_template('index.html')

@app.context_processor
def inject_notifications():
    if current_user.is_authenticated:
        # Query the database for the count of unread notifications for the current user
        unread_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
        # Make the count available to all templates with the variable name 'unread_notification_count'
        return dict(unread_notification_count=unread_count)
    # If no user is logged in, provide a default value of 0
    return dict(unread_notification_count=0)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
