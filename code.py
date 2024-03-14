from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='templates')

# Fonction pour initialiser la base de données en exécutant le script SQL depuis un fichier
def init_db():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    with open('table.sql', 'r') as f:
        cursor.executescript(f.read())
    conn.commit()
    conn.close()

init_db()

# Fonction pour ajouter un utilisateur à la base de données
def add_user(email, username, password_hash):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (email, username, password_hash) VALUES (?, ?, ?)
    ''', (email, username, password_hash))
    conn.commit()
    conn.close()

# Fonction pour récupérer un utilisateur par son email ou son username
def get_user(email_or_username):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE email=? OR username=?
    ''', (email_or_username, email_or_username))
    user = cursor.fetchone()
    conn.close()
    return user

# Fonction pour vérifier le mot de passe d'un utilisateur
def check_password(user, password):
    if user and check_password_hash(user[3], password):
        return True
    else:
        return False

@app.route('/')
def racine():
    return render_template('racine.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        return 'Les mots de passe ne correspondent pas. Veuillez réessayer.'

    existing_user = get_user(email)
    if existing_user:
        return 'Cet email est déjà utilisé. Veuillez en choisir un autre.'
    existing_username = get_user(username)
    if existing_username:
        return 'Ce pseudo est déjà utilisé. Veuillez en choisir un autre.'

    password_hash = generate_password_hash(password)
    add_user(email, username, password_hash)

    return 'Inscription réussie. Vous pouvez maintenant vous connecter.'

@app.route('/login', methods=['POST'])
def login_post():
    email_or_username = request.form['email_or_username']
    password = request.form['password']

    user = get_user(email_or_username)
    if check_password(user, password):
        return 'Connexion réussie.'
    else:
        return 'Identifiants incorrects. Veuillez réessayer.'

if __name__ == '__main__':
    app.run(debug=True)
