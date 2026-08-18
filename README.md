# AI Study Hub 

A Django MVT web application that helps students organize their tasks, notes, and
learning resources, with an integrated AI study assistant powered by Google Gemini.

## Features
- Authentication (register, email verification, login, logout, password reset)
- Study Planner: Tasks CRUD with priority, due date, status
- Notes with categories, tags, search, and pagination
- Learning Resources with types, JavaScript live search, and filtering
- AI Study Assistant with saved conversation history
- Dashboard with statistics and charts
- PDF export for tasks
- Profile with image upload, dark mode, responsive design

## Technologies
Python, Django (MVT), PostgreSQL, HTML5, CSS3, JavaScript, Bootstrap 5,
Chart.js, Google Gemini API, xhtml2pdf.

## Architecture (MVT)
Browser -> URL -> View -> Model -> Database -> View -> Template -> Browser
Apps: accounts, dashboard, planner, notes, resources, ai_assistant.

## Installation
1. git clone <your-repo-url> && cd AIStudyHub
2. python3 -m venv venv && source venv/bin/activate
3. pip install -r requirements.txt
4. Create a .env file (see below)
5. python manage.py migrate
6. python manage.py createsuperuser
7. python manage.py runserver

## Environment Variables (.env)
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=aistudyhub_db
DB_USER=aistudyhub_user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
GEMINI_API_KEY=your-gemini-api-key
EMAIL_USER=your-gmail@gmail.com
EMAIL_PASSWORD=your-gmail-app-password

## AI Setup
Get a free Gemini API key from https://aistudio.google.com and add it to .env.

## Email Setup
Uses Gmail SMTP. Requires a Gmail App Password (not your normal password).

## Admin Access
http://127.0.0.1:8000/admin/

## Screenshots
(Add screenshots here: dashboard, tasks, notes, AI chat, profile)

## ERD
See erd.png / ERD.md for the database diagram.

## Team Members
- Rawan Magdy
- (Second member name)

## Future Improvements
- Real-time AI streaming, notifications, calendar sync, mobile app