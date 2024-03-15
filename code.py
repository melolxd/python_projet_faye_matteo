from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__, template_folder='templates')

# Function to initialize the database by executing the SQL script from a file
def init_db():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    with open('table.sql', 'r') as f:
        cursor.executescript(f.read())
    conn.commit()
    conn.close()

init_db()

def validate_email(email):
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(regex, email)

def validate_password(password):
    # Au moins 6 caractères
    if len(password) < 6:
        return False
    # Au moins un chiffre
    if not any(char.isdigit() for char in password):
        return False
    # Au moins un symbole
    if not any(char.isalnum() for char in password):
        return False
    return True


# Function to add a user to the database
def add_user(email, username, password_hash):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (email, username, password_hash) VALUES (?, ?, ?)
    ''', (email, username, password_hash))
    conn.commit()
    conn.close()

# Function to retrieve a user by their email or username
def get_user(email_or_username):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE email=? OR username=?
    ''', (email_or_username, email_or_username))
    user = cursor.fetchone()
    conn.close()
    return user

# Function to check a user's password
def check_password(user, password):
    if user and check_password_hash(user[3], password):
        return True
    else:
        return False

@app.route('/')
def root():
    return render_template('root.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/discover')
def discover():
    return render_template('discover.html')


@app.route('/register', methods=['POST'])
def register_post():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    error_email = None
    error_username = None
    error_password = None
    error_confirm_password = None

    # Validation de l'email
    if not validate_email(email):
        error_email = 'Adresse email invalide.'

    # Validation du mot de passe
    if not validate_password(password):
        error_password = 'Le mot de passe doit avoir au moins 6 caractères, un chiffre et un symbole.'
    elif password != confirm_password:
        error_confirm_password = 'Les mots de passe ne correspondent pas.'

    # Si des erreurs sont présentes, les renvoyer à la page d'inscription
    if error_email or error_password or error_confirm_password:
        return render_template('register.html', error_email=error_email, error_username=error_username,
                               error_password=error_password, error_confirm_password=error_confirm_password)

    password_hash = generate_password_hash(password)
    add_user(email, username, password_hash)

    # Redirection vers la page de connexion après inscription réussie
    return redirect(url_for('login'))



@app.route('/login', methods=['POST'])
def login_post():
    email_or_username = request.form['email_or_username']
    password = request.form['password']
    error_email_or_username = None
    error_password = None

    user = get_user(email_or_username)
    if not user:
        error_email_or_username = 'Email ou pseudo incorrect.'
    elif not check_password(user, password):
        error_password = 'Mot de passe incorrect.'

    if error_email_or_username or error_password:
        return render_template('login.html', error_email_or_username=error_email_or_username, error_password=error_password)

    # Redirect to root page after successful login
    return redirect(url_for('discover'))


if __name__ == '__main__':
    app.run(debug=True)
