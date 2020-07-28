from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def present_login():
    return render_template('login.html')

@app.route('/home')
def home_page():
    return render_template('home.html')

if __name__ == '__main__':
    app.run()
