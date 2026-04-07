from extensions import db
from models import User, Ticket, TicketHistory
from datetime import datetime, timedelta


def seed_database(app=None):

    # create 10 users (2 admins, 8 employees)
    users = [
        User(username='admin', email='admin@altido.com', role='admin'),
        User(username='sarah.jones', email='sarah.jones@altido.com', role='admin'),
        User(username='james.smith', email='james.smith@altido.com', role='employee'),
        User(username='emma.wilson', email='emma.wilson@altido.com', role='employee'),
        User(username='david.brown', email='david.brown@altido.com', role='employee'),
        User(username='lucy.taylor', email='lucy.taylor@altido.com', role='employee'),
        User(username='mark.davies', email='mark.davies@altido.com', role='employee'),
        User(username='sophie.evans', email='sophie.evans@altido.com', role='employee'),
        User(username='tom.harris', email='tom.harris@altido.com', role='employee'),
        User(username='hannah.clark', email='hannah.clark@altido.com', role='employee'),
    ]

    # set password for all users (password is "password123")
    for user in users:
        user.set_password('password123')

    db.session.add_all(users)
    db.session.commit()

    # create 10 tickets with varied statuses and priorities
    base_date = datetime(2026, 3, 1, 9, 0, 0)
    tickets = [
        Ticket(
            title='CRM login page not loading',
            description='The login page for the CRM system returns a blank screen on Chrome. Other browsers seem fine.',
            status='open', priority='high',
            created_by=3, assigned_to=1,
            created_at=base_date
        ),
        Ticket(
            title='Update customer contact form fields',
            description='Need to add a mobile phone field to the customer contact form as per the new requirements.',
            status='in_progress', priority='medium',
            created_by=4, assigned_to=3,
            created_at=base_date + timedelta(days=1)
        ),
        Ticket(
            title='Report export failing for large datasets',
            description='When exporting more than 5000 records to CSV the process times out and no file is downloaded.',
            status='open', priority='high',
            created_by=5, assigned_to=2,
            created_at=base_date + timedelta(days=2)
        ),
        Ticket(
            title='Add search bar to contacts list',
            description='Users have requested a search bar at the top of the contacts list page to find records quickly.',
            status='closed', priority='medium',
            created_by=6, assigned_to=4,
            created_at=base_date + timedelta(days=3)
        ),
        Ticket(
            title='Database backup schedule review',
            description='The current backup schedule runs at midnight but the team wants it moved to 2am to avoid peak hours.',
            status='open', priority='low',
            created_by=7, assigned_to=None,
            created_at=base_date + timedelta(days=4)
        ),
        Ticket(
            title='Password reset email not sending',
            description='Customers report that the password reset email never arrives. Checked spam folders already.',
            status='in_progress', priority='high',
            created_by=8, assigned_to=1,
            created_at=base_date + timedelta(days=5)
        ),
        Ticket(
            title='Dashboard charts showing wrong month',
            description='The sales dashboard is displaying March data instead of April. Likely a date calculation bug.',
            status='open', priority='medium',
            created_by=9, assigned_to=3,
            created_at=base_date + timedelta(days=6)
        ),
        Ticket(
            title='New starter account setup request',
            description='Please create accounts for two new starters joining the support team next Monday.',
            status='closed', priority='low',
            created_by=10, assigned_to=2,
            created_at=base_date + timedelta(days=7)
        ),
        Ticket(
            title='API rate limiting needs adjustment',
            description='Third party integrations are hitting our rate limit too often. Need to increase from 100 to 500 per minute.',
            status='in_progress', priority='medium',
            created_by=3, assigned_to=1,
            created_at=base_date + timedelta(days=8)
        ),
        Ticket(
            title='Accessibility improvements for main navigation',
            description='Screen readers cannot properly read the main navigation menu. Need to add ARIA labels throughout.',
            status='open', priority='medium',
            created_by=5, assigned_to=None,
            created_at=base_date + timedelta(days=9)
        ),
    ]

    db.session.add_all(tickets)
    db.session.commit()

    # create ticket history entries (at least 10)
    history_entries = [
        TicketHistory(ticket_id=1, changed_by=3, action='Ticket created', new_value='CRM login page not loading',
                      changed_at=base_date),
        TicketHistory(ticket_id=1, changed_by=1, action='Assigned to changed', old_value='Unassigned', new_value='admin',
                      changed_at=base_date + timedelta(hours=2)),
        TicketHistory(ticket_id=2, changed_by=4, action='Ticket created', new_value='Update customer contact form fields',
                      changed_at=base_date + timedelta(days=1)),
        TicketHistory(ticket_id=2, changed_by=2, action='Status changed', old_value='open', new_value='in_progress',
                      changed_at=base_date + timedelta(days=1, hours=4)),
        TicketHistory(ticket_id=3, changed_by=5, action='Ticket created', new_value='Report export failing for large datasets',
                      changed_at=base_date + timedelta(days=2)),
        TicketHistory(ticket_id=4, changed_by=6, action='Ticket created', new_value='Add search bar to contacts list',
                      changed_at=base_date + timedelta(days=3)),
        TicketHistory(ticket_id=4, changed_by=2, action='Status changed', old_value='open', new_value='in_progress',
                      changed_at=base_date + timedelta(days=3, hours=3)),
        TicketHistory(ticket_id=4, changed_by=2, action='Status changed', old_value='in_progress', new_value='closed',
                      changed_at=base_date + timedelta(days=5)),
        TicketHistory(ticket_id=5, changed_by=7, action='Ticket created', new_value='Database backup schedule review',
                      changed_at=base_date + timedelta(days=4)),
        TicketHistory(ticket_id=6, changed_by=8, action='Ticket created', new_value='Password reset email not sending',
                      changed_at=base_date + timedelta(days=5)),
        TicketHistory(ticket_id=6, changed_by=1, action='Priority changed', old_value='medium', new_value='high',
                      changed_at=base_date + timedelta(days=5, hours=1)),
        TicketHistory(ticket_id=6, changed_by=1, action='Status changed', old_value='open', new_value='in_progress',
                      changed_at=base_date + timedelta(days=5, hours=2)),
    ]

    db.session.add_all(history_entries)
    db.session.commit()

    print('Database seeded successfully.')
    print(f'Created {len(users)} users, {len(tickets)} tickets, {len(history_entries)} history entries.')
    print('Default login: admin / password123')


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_database(app)
