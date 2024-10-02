# Flask Todo App with User Authentication

This is a simple Flask-based web application that allows users to register, log in, and manage their to-do tasks. The app features user authentication, task creation, task completion, and task deletion functionality.

## Features

- **User Registration**: Users can sign up with a username and password.
- **User Login**: Registered users can log in to the application.
- **Task Management**: Authenticated users can add, complete, and delete their tasks.
- **User-Specific Data**: Each user's tasks are private and accessible only to them.
- **Flash Messages**: Informative messages are displayed for actions like login success, invalid login, registration success, etc.
  
## Technology Stack

- **Backend**: Python, Flask, Flask-Login for session management.
- **Database**: SQLite (SQLAlchemy ORM).
- **Frontend**: HTML (rendered using Jinja2 templates).
- **Forms**: Flask-WTF for form validation and CSRF protection.

## Installation

Follow the steps below to set up the project locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/todo-flask-app.git
   cd todo-flask-app
