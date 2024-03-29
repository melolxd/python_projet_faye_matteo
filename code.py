from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__, template_folder='templates')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Function to initialize the database by executing the SQL script from a file
def init_db():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    with open('table.sql', 'r') as f:
        cursor.executescript(f.read())
    conn.commit()
    conn.close()

def validate_email(email):
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(regex, email)

def validate_password(password):
    # At least 6 characters
    if len(password) < 6:
        return False
    # At least one digit
    if not any(char.isdigit() for char in password):
        return False
    # At least one symbol
    if not any(not char.isalnum() for char in password):
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
    if 'user_id' in session:
        return redirect(url_for('discover'))
    else:
        return render_template('root.html')

@app.route('/login')
def login():
    if 'user_id' in session:
        return redirect(url_for('discover'))
    else:
        return render_template('login.html')

@app.route('/register')
def register():
    if 'user_id' in session:
        return redirect(url_for('discover'))
    else:
        return render_template('register.html')

@app.route('/discover')
def discover():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('discover.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/logout-confirm', methods=['POST'])
def logout_confirm():
    session.pop('user_id', None)
    return redirect(url_for('root'))

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

    # Validate email
    if not validate_email(email):
        error_email = 'Invalid email address.'
    elif get_user(email):
        error_email = 'This email address is already in use.'

    # Validate password
    if not validate_password(password):
        error_password = 'Password must contain at least 6 characters, a digit and a symbol.'
    elif password != confirm_password:
        error_confirm_password = 'Passwords do not match.'

    # If errors present, return to registration page
    if error_email or error_password or error_confirm_password:
        return render_template('register.html', error_email=error_email, error_username=error_username,
                               error_password=error_password, error_confirm_password=error_confirm_password)

    password_hash = generate_password_hash(password)
    add_user(email, username, password_hash)

    # Redirect to login page after successful registration
    return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def login_post():
    email_or_username = request.form['email_or_username']
    password = request.form['password']
    error_email_or_username = None
    error_password = None

    user = get_user(email_or_username)
    if not user:
        error_email_or_username = 'Incorrect email or username.'
    elif not check_password(user, password):
        error_password = 'Incorrect password'
    else:
        session['user_id'] = user[0]

    if error_email_or_username or error_password:
        return render_template('login.html', error_email_or_username=error_email_or_username, error_password=error_password)

    # Redirect to root page after successful login
    return redirect(url_for('root'))

@app.route('/write-article', methods=['GET', 'POST'])
def write_article():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author_id = session['user_id']

        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO articles (title, content, author_id) VALUES (?, ?, ?)
        ''', (title, content, author_id))
        conn.commit()
        conn.close()

        return redirect(url_for('discover'))
    else:
        return render_template('write-article.html')

@app.route('/articles')
def articles():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT articles.id, articles.title, articles.content, users.username
        FROM articles
        INNER JOIN users ON articles.author_id = users.id
        ORDER BY articles.created_at DESC
    ''')
    articles = cursor.fetchall()
    conn.close()
    return render_template('articles.html', articles=articles)

def add_comment(article_id, user_id, content):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO comments (article_id, user_id, content) VALUES (?, ?, ?)
    ''', (article_id, user_id, content))
    conn.commit()
    conn.close()

def get_comments_by_article_id(article_id):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT comments.id, comments.content, users.username
        FROM comments
        INNER JOIN users ON comments.user_id = users.id
        WHERE comments.article_id = ?
        ORDER BY comments.created_at DESC
    ''', (article_id,))
    comments = cursor.fetchall()
    conn.close()
    return comments

@app.route('/articles/<int:article_id>')
def article(article_id):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT articles.id, articles.title, articles.content, users.username
        FROM articles
        INNER JOIN users ON articles.author_id = users.id
        WHERE articles.id = ?
    ''', (article_id,))
    article = cursor.fetchone()
    conn.close()

    comments = get_comments_by_article_id(article_id)

    return render_template('article.html', article=article, comments=comments)

@app.route('/articles/<int:article_id>/comments', methods=['POST'])
def add_article_comment(article_id):
    content = request.form['content']
    user_id = session['user_id']

    add_comment(article_id, user_id, content)

    return redirect(url_for('article', article_id=article_id))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
