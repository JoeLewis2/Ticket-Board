from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from extensions import db
from models import Ticket, TicketHistory, User

tickets_bp = Blueprint('tickets', __name__)


# dashboard - main page showing tickets
@tickets_bp.route('/')
@login_required
def dashboard():
    # get optional status filter from query string
    status_filter = request.args.get('status', 'all')

    # admin sees all tickets. employee sees only their own
    if current_user.is_admin():
        query = Ticket.query
    else:
        query = Ticket.query.filter_by(created_by=current_user.id)

    # apply status filter if one is selected
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)

    tickets = query.order_by(Ticket.created_at.desc()).all()
    return render_template('dashboard.html', tickets=tickets, status_filter=status_filter)


# view a single ticket with its history
@tickets_bp.route('/tickets/<int:ticket_id>')
@login_required
def view_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    # employees can view only tickets assigneed to them
    if not current_user.is_admin() and ticket.created_by != current_user.id:
        abort(403)

    return render_template('view_ticket.html', ticket=ticket)


# create a new ticket
@tickets_bp.route('/tickets/create', methods=['GET', 'POST'])
@login_required
def create_ticket():
    # get list of users for the assigned_to dropdown (admin only)
    users = User.query.all() if current_user.is_admin() else []

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        priority = request.form.get('priority', 'medium')
        assigned_to = request.form.get('assigned_to', '')

        # validate required fields
        if not title:
            flash('Title is required.', 'danger')
            return render_template('create_ticket.html', users=users)

        if len(title) > 150:
            flash('Title must be 150 characters or less.', 'danger')
            return render_template('create_ticket.html', users=users)

        if not description:
            flash('Description is required.', 'danger')
            return render_template('create_ticket.html', users=users)

        if priority not in ['low', 'medium', 'high']:
            flash('Invalid priority selected.', 'danger')
            return render_template('create_ticket.html', users=users)

        # create the ticket
        ticket = Ticket(
            title=title,
            description=description,
            priority=priority,
            created_by=current_user.id,
            assigned_to=int(assigned_to) if assigned_to else None
        )
        db.session.add(ticket)
        db.session.flush()

        # add a history entry for the creation
        history = TicketHistory(
            ticket_id=ticket.id,
            changed_by=current_user.id,
            action='Ticket created',
            new_value=title
        )
        db.session.add(history)
        db.session.commit()

        flash('Ticket created successfully.', 'success')
        return redirect(url_for('tickets.dashboard'))

    return render_template('create_ticket.html', users=users)


# edit an existing ticket
@tickets_bp.route('/tickets/<int:ticket_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    # employees can only edit their own tickets
    if not current_user.is_admin() and ticket.created_by != current_user.id:
        abort(403)

    users = User.query.all() if current_user.is_admin() else []

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()

        # validate required fields
        if not title:
            flash('Title is required.', 'danger')
            return render_template('edit_ticket.html', ticket=ticket, users=users)

        if len(title) > 150:
            flash('Title must be 150 characters or less.', 'danger')
            return render_template('edit_ticket.html', ticket=ticket, users=users)

        if not description:
            flash('Description is required.', 'danger')
            return render_template('edit_ticket.html', ticket=ticket, users=users)

        # track changes for history
        if ticket.title != title:
            history = TicketHistory(
                ticket_id=ticket.id, changed_by=current_user.id,
                action='Title changed', old_value=ticket.title, new_value=title
            )
            db.session.add(history)
            ticket.title = title

        if ticket.description != description:
            history = TicketHistory(
                ticket_id=ticket.id, changed_by=current_user.id,
                action='Description changed', old_value='(previous description)', new_value='(updated description)'
            )
            db.session.add(history)
            ticket.description = description

        # admin-only fields
        if current_user.is_admin():
            new_status = request.form.get('status', ticket.status)
            new_priority = request.form.get('priority', ticket.priority)
            assigned_to = request.form.get('assigned_to', '')

            # validate feilds
            if new_status not in ['open', 'in_progress', 'closed']:
                flash('Invalid status selected.', 'danger')
                return render_template('edit_ticket.html', ticket=ticket, users=users)

            if new_priority not in ['low', 'medium', 'high']:
                flash('Invalid priority selected.', 'danger')
                return render_template('edit_ticket.html', ticket=ticket, users=users)

            if ticket.status != new_status:
                history = TicketHistory(
                    ticket_id=ticket.id, changed_by=current_user.id,
                    action='Status changed', old_value=ticket.status, new_value=new_status
                )
                db.session.add(history)
                ticket.status = new_status

            if ticket.priority != new_priority:
                history = TicketHistory(
                    ticket_id=ticket.id, changed_by=current_user.id,
                    action='Priority changed', old_value=ticket.priority, new_value=new_priority
                )
                db.session.add(history)
                ticket.priority = new_priority

            # track assignment change
            new_assigned = int(assigned_to) if assigned_to else None
            if ticket.assigned_to != new_assigned:
                old_assignee = ticket.assignee.username if ticket.assignee else 'Unassigned'
                new_assignee_user = User.query.get(new_assigned) if new_assigned else None
                new_assignee_name = new_assignee_user.username if new_assignee_user else 'Unassigned'
                history = TicketHistory(
                    ticket_id=ticket.id, changed_by=current_user.id,
                    action='Assigned to changed', old_value=old_assignee, new_value=new_assignee_name
                )
                db.session.add(history)
                ticket.assigned_to = new_assigned

        db.session.commit()
        flash('Ticket updated successfully.', 'success')
        return redirect(url_for('tickets.view_ticket', ticket_id=ticket.id))

    return render_template('edit_ticket.html', ticket=ticket, users=users)


# delete a ticket (admin only)
@tickets_bp.route('/tickets/<int:ticket_id>/delete', methods=['POST'])
@login_required
def delete_ticket(ticket_id):
    if not current_user.is_admin():
        abort(403)

    ticket = Ticket.query.get_or_404(ticket_id)

    # delete related history entries
    TicketHistory.query.filter_by(ticket_id=ticket.id).delete()
    db.session.delete(ticket)
    db.session.commit()

    flash('Ticket deleted successfully.', 'success')
    return redirect(url_for('tickets.dashboard'))
