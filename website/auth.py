from flask import Blueprint, render_template, flash, request
import re

auth = Blueprint('auth', __name__)

def is_valid_name(full_name):
    return bool(re.match(r"^[A-Za-z\s\-']+$", full_name)) and len(full_name.split()) >= 2

def is_valid_email(email):
    # Add: Check if email doesnt already exist in the database
    pattern = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

def is_strong_password(password):
    if len(password) < 8:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char in "!@#$%^&*()-_=+[]{}|;:',.<>?/`~" for char in password):
        return False
    return True

def passwords_match(password, confirm_password):
    return password == confirm_password


@auth.route('/login')
def login():
  return render_template('login.html')

@auth.route('/logout')
def logout():
  return "<p>logout</p>"

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():

  if request.method == 'POST':
    email = request.form.get('email')
    fullName = request.form.get('fullName')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    if not is_valid_name(fullName):
      flash('Invalid name. Provide a first and last name (no numbers or symbols allowed).', category='error')
    elif not is_valid_email(email):
      flash('Invalid email. Example format: test@email.com', category='error')
    elif not is_strong_password(password1):
      flash('Password must be at least 8 characters, include uppercase, lowercase, a number, and a special character.', category='error')
    elif not passwords_match(password1, password2):
      flash('Passwords do not match.', category='error')
    else:
      flash('Account has been created!', category='success')

  return render_template('sign_up.html')
