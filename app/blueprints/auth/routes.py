from . import bp as app
from app.blueprints.main.models import User
from app import db, login_manager
from flask import redirect, url_for, render_template, request, flash
from flask_login import login_user, logout_user, current_user, login_required



@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    password = request.form['password']
    next_url = request.form['next']

    user = User.query.filter_by(email=email).first()

    if user is None:
        flash(f'User with email {email} does not exist.', 'danger')
    elif user.check_my_password(password):
        login_user(user)
        flash(f'Welcome back {user.username}', 'success')
        if next_url != '':
            return redirect(next_url)
        return redirect(url_for('main.home'))
    else:
        # user exists but password is wrong
        flash(f'Password is incorrect', 'danger')

    return render_template('login.html')


@app.route('/register', methods= ["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    confirmpassword = request.form['confirmPassword']


    check_user = User.query.filter_by(email=email).first()
    if check_user is not None:
        flash(f'User with email {email} already exists', 'danger')

    elif password != confirmpassword:
        flash('Passwords do not match', "danger")
    else:
        #User can be created
        try: 
            new_user = User(email=email, username=username, password='')
            new_user.hash_my_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('User created successfullly', 'success')
            return redirect(url_for('auth.login'))
        except:
            flash('There was an error', 'danger')
    return render_template('register.html')

@app.route('/logout')
def logout():
    flash("Logged out successfully", 'success')
    logout_user()

    return redirect(url_for('auth.login'))

@app.route('/reset-password', methods=["GET", "POST"])
@login_required
def reset_password():
    if request.method == 'GET':
        return render_template('reset-password.html')

    old_password = request.form['oldPassword']
    new_password = request.form['newPassword']
    confirm_new_passord = request.form['confirmNewPassword']

    if not current_user.check_my_password(old_password):
        flash("Old password not correct", 'danger')

    elif new_password == confirm_new_passord:
        current_user.hash_my_password(new_password)
        db.session.add(current_user)
        db.session.commit()
        return render_template('reset-password.html')

    flash("Passwords do not match.", 'danger')
    return render_template('reset-password.html.j2')
