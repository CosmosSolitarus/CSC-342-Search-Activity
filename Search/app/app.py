from flask import Flask, render_template, redirect, url_for

app = Flask(__name__, template_folder='../www/templates', static_folder='../www/static')

@app.route('/')
def index():
    return render_template('home.html')

# Redirect '/home' to '/'
@app.route('/home')
def redirect_home():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
