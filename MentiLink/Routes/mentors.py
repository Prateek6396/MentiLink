# In Routes/mentors.py
from flask import Blueprint, render_template, request
from flask_login import login_required
from models.user import User
from sqlalchemy import or_

mentors_bp = Blueprint('mentors', __name__)

@mentors_bp.route('/find')
@login_required
def find_mentor():
    # Get search and filter parameters from the URL
    query = request.args.get('query', '')
    expertise = request.args.get('expertise', '')

    # Start with a base query for all mentors
    mentors_query = User.query.filter_by(role='mentor')

    # Apply search filter if a query is provided
    if query:
        search_term = f"%{query}%"
        mentors_query = mentors_query.filter(
            or_(
                User.full_name.ilike(search_term),
                User.expertise.ilike(search_term),
                User.bio.ilike(search_term)
            )
        )
    
    # Apply expertise filter if provided
    if expertise:
        mentors_query = mentors_query.filter(User.expertise.ilike(f"%{expertise}%"))

    mentors = mentors_query.all()
    
    return render_template('find_mentor.html', mentors=mentors, query=query, expertise=expertise)