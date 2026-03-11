from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.user import User
from models.session import Session
from models.slot import Slot, db
from models.goal import Goal
from datetime import datetime, timedelta
from flask_mail import Message
from extensions import mail
from pytz import timezone
import secrets

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    # --- MENTOR-SPECIFIC LOGIC ---
    if current_user.role == 'mentor':
        # Get the mentor's upcoming sessions that are already booked
        upcoming_sessions = Session.query.join(Slot).filter(
            Session.mentor_id == current_user.id,
            Session.status == 'scheduled',
            Slot.start_time > datetime.utcnow()
        ).order_by(Slot.start_time).all()

        # Calculate statistics for the mentor
        stats = {
            'total_slots': Slot.query.filter_by(mentor_id=current_user.id).count(),
            'booked_sessions': Session.query.filter_by(mentor_id=current_user.id).count(),
            'completed_sessions': Session.query.filter_by(mentor_id=current_user.id, status='completed').count(),
            'available_slots': Slot.query.filter_by(mentor_id=current_user.id, is_available=True).count()
        }

        return render_template('dashboard.html',
                             upcoming_sessions=upcoming_sessions,
                             stats=stats)

    # --- STUDENT-SPECIFIC LOGIC ---
    else:
        # Get the student's upcoming sessions
        upcoming_sessions = Session.query.join(Slot).filter(
            Session.student_id == current_user.id,
            Session.status == 'scheduled',
            Slot.start_time > datetime.utcnow()
        ).order_by(Slot.start_time).all()

        # Get all available slots from all mentors
        available_slots = Slot.query.filter(
            Slot.is_available == True,
            Slot.start_time > datetime.utcnow()
        ).order_by(Slot.start_time).all()

        # Calculate statistics for the student
        stats = {
            'total_sessions': Session.query.filter_by(student_id=current_user.id).count(),
            'completed_sessions': Session.query.filter_by(student_id=current_user.id, status='completed').count(),
            'upcoming_sessions': len(upcoming_sessions)
        }
        
        return render_template('dashboard.html',
                             upcoming_sessions=upcoming_sessions,
                             available_slots=available_slots,
                             stats=stats)


@dashboard_bp.route('/available_slots')
@login_required
def available_slots():
    if current_user.role != 'student':
        return jsonify({'error': 'Unauthorized'}), 403
    
    slots = Slot.query.filter_by(is_available=True).filter(
        Slot.start_time > datetime.utcnow()
    ).all()
    
    slots_data = []
    for slot in slots:
        slots_data.append({
            'id': slot.id,
            'mentor_name': slot.mentor_user.full_name,
            'title': slot.title,
            'description': slot.description,
            'start_time': slot.start_time.strftime('%Y-%m-%d %H:%M'),
            'end_time': slot.end_time.strftime('%Y-%m-%d %H:%M')
        })
    
    return jsonify(slots_data)

from datetime import timedelta

@dashboard_bp.route('/create_slot', methods=['GET', 'POST'])
@login_required
def create_slot():
    if current_user.role != 'mentor':
        flash('Only mentors can create slots.', 'danger')
        return redirect(url_for('dashboard.dashboard'))

    if request.method == 'POST':
        start_time_str = request.form.get('start_time')
        duration_min = int(request.form.get('duration'))
        is_recurring = request.form.get('is_recurring')
        repeat_count = int(request.form.get('repeat_count', 1))

        # 1. Parse the naive datetime string from the form (e.g., "2025-10-13T14:30")
        # This naive time IS our IST time.
        initial_start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
        
        if not is_recurring:
            repeat_count = 1

        slots_created = 0
        for i in range(repeat_count):
            start_time = initial_start_time + timedelta(weeks=i)
            end_time = start_time + timedelta(minutes=duration_min)

            # 2. Save the naive IST time directly into the database
            new_slot = Slot(
                mentor_id=current_user.id,
                start_time=start_time,
                end_time=end_time
            )
            db.session.add(new_slot)
            slots_created += 1

        db.session.commit()
        flash(f'{slots_created} new availability slot(s) created successfully!', 'success')
        return redirect(url_for('dashboard.dashboard'))

    return render_template('create_slot.html')


@dashboard_bp.route('/book_session/<int:slot_id>', methods=['POST'])
@login_required
def book_session(slot_id):
    if current_user.role != 'student':
        flash('Only students can book sessions.', 'danger')
        return redirect(url_for('dashboard.dashboard'))

    slot_to_book = Slot.query.get_or_404(slot_id)

    if not slot_to_book.is_available:
        flash('This slot has already been booked.', 'warning')
        return redirect(url_for('dashboard.dashboard'))

    # --- THIS IS THE CORRECTED TIME CHECK ---
    IST = timezone('Asia/Kolkata')
    
    # 1. Get the current time in IST (e.g., 14:25+05:30)
    now_in_ist = datetime.now(IST)
    
    # 2. Get the naive time from DB and make it IST-aware (e.g., 14:30 -> 14:30+05:30)
    slot_start_time_ist = IST.localize(slot_to_book.start_time)

    # 3. Compare two timezone-aware datetimes. This is reliable.
    if now_in_ist > slot_start_time_ist:
        flash('This time slot has already passed and cannot be booked.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
        
    room_name = secrets.token_hex(16)
    meeting_link = f"https://meet.jit.si/{room_name}"

    # Create the new session, including the link
    session = Session(
        mentor_id=slot_to_book.mentor_id,
        student_id=current_user.id,
        slot_id=slot_to_book.id,
        meeting_link=meeting_link, # <-- SAVE THE LINK
        title=f"Mentoring Session with {slot_to_book.mentor_user.full_name}",
        description="Initial session booking."
    )
    
    slot_to_book.is_available = False
    db.session.add(session)
    db.session.commit()
    
    if not slot_to_book.is_available:
        flash('This slot has already been booked.', 'warning')
        return redirect(url_for('dashboard.dashboard'))

    # Define IST and get the current time in IST
    IST = timezone('Asia/Kolkata')
    now_in_ist = datetime.now(IST)

    # Make the database time IST-aware for a correct comparison
    slot_start_time_ist = IST.localize(slot_to_book.start_time)

    if now_in_ist > slot_start_time_ist:
        flash('This time slot has already passed and cannot be booked.', 'danger')
        return redirect(url_for('dashboard.dashboard'))

    # Create the new session
    session = Session(
        mentor_id=slot_to_book.mentor_id,
        student_id=current_user.id,
        slot_id=slot_to_book.id,
        # FIX IS ON THE NEXT LINE
        title=f"Mentoring Session with {slot_to_book.mentor_user.full_name}",
        description="Initial session booking."
    )
    
    # Mark the slot as unavailable
    slot_to_book.is_available = False

    db.session.add(session)
    db.session.commit()
    try:
        # Email to student
        msg_student = Message(
            'Session Booking Confirmation',
            recipients=[current_user.email]
        )
        msg_student.body = f"Hello {current_user.full_name},\n\nYour session with {slot_to_book.mentor_user.full_name} on {slot_to_book.start_time.strftime('%Y-%m-%d at %H:%M')} has been successfully booked.\n\nRegards,\nMentiLink Team"
        mail.send(msg_student)

        # Email to mentor
        msg_mentor = Message(
            'New Session Booked!',
            recipients=[slot_to_book.mentor_user.email]
        )
        msg_mentor.body = f"Hello {slot_to_book.mentor_user.full_name},\n\nA new session has been booked by {current_user.full_name} for {slot_to_book.start_time.strftime('%Y-%m-%d at %H:%M')}.\n\nPlease check your dashboard for details.\n\nRegards,\nMentiLink Team"
        mail.send(msg_mentor)
    except Exception as e:
        flash(f"Session booked, but failed to send email notification: {e}", "warning")

    flash('Session booked successfully!', 'success')
    return redirect(url_for('dashboard.dashboard'))

@dashboard_bp.route('/my_slots')
@login_required
def my_slots():
    if current_user.role != 'mentor':
        flash('This page is only accessible to mentors.', 'danger')
        return redirect(url_for('dashboard.dashboard'))

    # Get the status filter from the URL
    status_filter = request.args.get('status')
    
    # Start with the base query
    query = Slot.query.filter_by(mentor_id=current_user.id)

    # Apply filter if one is provided
    if status_filter == 'available':
        query = query.filter_by(is_available=True)
        page_title = "My Available Slots"
    else:
        page_title = "All My Created Slots"

    all_slots = query.order_by(Slot.created_at.desc()).all()

    return render_template('my_slots.html', slots=all_slots, page_title=page_title)

@dashboard_bp.route('/delete_slot/<int:slot_id>', methods=['POST'])
@login_required
def delete_slot(slot_id):
    slot_to_delete = Slot.query.get_or_404(slot_id)

    # Security check: ensure the slot belongs to the current mentor
    if slot_to_delete.mentor_id != current_user.id:
        flash('You are not authorized to delete this slot.', 'danger')
        return redirect(url_for('dashboard.my_slots'))

    # Business rule: do not allow deletion of booked slots
    if not slot_to_delete.is_available:
        flash('You cannot delete a slot that has already been booked.', 'warning')
        return redirect(url_for('dashboard.my_slots'))

    db.session.delete(slot_to_delete)
    db.session.commit()

    flash('Slot has been deleted successfully.', 'success')
    return redirect(url_for('dashboard.my_slots'))

@dashboard_bp.route('/goal/add', methods=['POST'])
@login_required
def add_goal():
    if current_user.role == 'student':
        description = request.form.get('description')
        if description:
            new_goal = Goal(user_id=current_user.id, description=description)
            db.session.add(new_goal)
            db.session.commit()
            flash('New goal added!', 'success')
    return redirect(url_for('dashboard.dashboard'))

@dashboard_bp.route('/goal/update/<int:goal_id>', methods=['POST'])
@login_required
def update_goal_status(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.user_id == current_user.id:
        new_status = request.form.get('status')
        if new_status in ['In Progress', 'Completed']:
            goal.status = new_status
            db.session.commit()
            flash(f'Goal marked as {new_status}!', 'info')
    return redirect(url_for('dashboard.dashboard'))

@dashboard_bp.route('/goal/delete/<int:goal_id>', methods=['POST'])
@login_required
def delete_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.user_id == current_user.id:
        db.session.delete(goal)
        db.session.commit()
        flash('Goal has been deleted.', 'success')
    return redirect(url_for('dashboard.dashboard'))