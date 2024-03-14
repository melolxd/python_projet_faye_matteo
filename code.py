from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route('/')
def racine():
    return render_template('racine.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/discover')
def discover():
    return render_template('discover.html')

if __name__ == '__main__':
    app.run(debug=True)
