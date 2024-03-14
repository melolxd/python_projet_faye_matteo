from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/discover')
def discover():
    return render_template('discover.html')

if __name__ == '__main__':
    app.run(debug=True)
