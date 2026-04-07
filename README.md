Ticket Board 
=========== 

A simple support ticket tracking web app, written using Flask and SQLite.
Built for Altido Group Ltd internal helpdesk and support requests to allow staff
members to raise requests with different priorities and statuses. Uses role-based 
permissions to allow different levels of access to different parts of the site.

Features: 
--------- 
- Users may register/login with login credentials. 
- Users may be either Admin or Employee role.
- Users can raise/edit/view/delete support tickets (depending on permissions).
- Tickets have statuses (Open, In Progress, Closed). 
- Tickets have priorities (Low, Medium, High). 
- Tickets can be assigned to different users (Admin only).
- Audit history keeps track of all edits to tickets.

Role Permissions Table: 
----------------------- 
| | Admin | Employee | 
|-------------------------------|-------|----------| 
| Can view ALL tickets | Yes | No | 
| Can create new tickets | Yes | Yes | 
| Can edit ANY ticket | Yes | No | 
| Can edit tickets created BYSELF| Yes | Yes | 
| Can change status/priority | Yes | No | 
| Can assign tickets | Yes | No | 
| Can delete tickets | Yes | No | 


Dependencies: 
------------- 
- Python 3.8+ 
- Flask 3.0.0 
- Flask-SQLAlchemy 3.0.5 
- Flask-Login 0.6.3 
- gunicorn 21.2.0 (required for production deployment to platforms like Heroku)
- python-dotenv 1.0.0 

To run locally: 
--------------- 

1. Install dependencies: `pip install -r requirements.txt` 
2. Seed database with sample data: `python seed.py` 
3. Run application: `python app.py` 
4. Open your browser to <http://127.0.0.1:5000> 

Default Login Credentials 
-------------------------- 
The seed script adds ten users which you can login with.

Username | Password | Role 
-------- | -------- | ------ 
admin | password123 | Admin 
sarah.jones | password123 | Admin 
james.smith | password123 | Employee 
emma.wilson | password123 | Employee 
david.brown | password123 | Employee 
lucy.taylor | password123 | Employee 
mark.davies | password123 | Employee 
sophie.evans | password123 | Employee 
tom.harris | password123 | Employee 
hannah.clark | password123 | Employee 

All passwords are: `password123` 

Structure 
--------- 
``` 
Ticket-Board/ 
├── app.py # Application factory and boilerplate setup 
├── config.py # Config settings 
├── models.py # Database models 
├── auth.py # Auth routes 
├── tickets.py # Ticket CRUD routes 
├── seed.py # Database seed script 
├── requirements.txt # Python dependencies 
├── Procfile # Used by Render to know how to deploy
├── templates/ # HTML templates 
│ ├── base.html 
│ ├── login.html 
│ ├── register.html 
│ ├── dashboard.html 
│ ├── create_ticket.html 
│ ├── edit_ticket.html 
│ └── view_ticket.html 
└── instance/ 
└── tickets.db # SQLite database file (created when running app)
``` 