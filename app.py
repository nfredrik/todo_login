from flask import Flask, render_template, redirect, url_for, request, flash, Response
from flask_login import  login_user, login_required, logout_user, current_user
from sqlalchemy.orm import Session


from database import db, app, login_manager
from models import User, Todo
from forms import LoginForm, RegistrationForm, TodoForm

# --- Login Manager ---
@login_manager.user_loader
def load_user(user_id:str) -> User:
    return User.query.get(int(user_id))
# --- Routes ---
@app.route(rule= '/register', methods=['GET', 'POST'])
def register() -> str | Response:
    form = RegistrationForm()
    if form.validate_on_submit():
        # 3. Check if username already exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists. Choose a different one.', 'error')
            return redirect(url_for('register'))

        # 4. Create a new user
        new_user = User(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route(rule = '/login', methods=['GET', 'POST'])
def login() -> Response | str :
    form = LoginForm()
    if form.validate_on_submit():

        # 3. The application queries the database to find a user with 
        #  the provided username
        user = User.query.filter_by(username=form.username.data).first()

        # 4. the application checks if the provided password matches 
        # the stored password
        if user and user.password == form.password.data:
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html', form=form)

@app.route(rule= '/logout')
@login_required
def logout() -> Response:
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required  # Restrict access to authenticated users only
def index() -> Response | str:
    form = TodoForm()
    if form.validate_on_submit():
        new_task = Todo(task=form.task.data, owner=current_user)
        db.session.add(new_task)
        db.session.commit()
        flash('Task Added Successfully!', 'success')
        return redirect(url_for('index'))

    tasks = Todo.query.filter_by(owner=current_user).all()
    return render_template('index.html', form=form, tasks=tasks)

@app.route('/complete/<int:task_id>')
@login_required
def complete_task(task_id:str) -> str:
    task = Todo.query.get_or_404(task_id)
    if task.owner != current_user:
        flash("You don't have permission to complete this task", 'error')
        return redirect(url_for('index'))
    task.complete = True
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id:str):
    task = Todo.query.get_or_404(task_id)
    if task.owner != current_user:
        flash("You don't have permission to delete this task", 'error')
        return redirect(url_for('index'))
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

# --- Initialize DB and Run App ---
if __name__ == '__main__':
    # Create the database
    with app.app_context():
        db.create_all()
    app.run(debug=True)
