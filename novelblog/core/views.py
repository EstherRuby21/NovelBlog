from flask import render_template, Blueprint

core = Blueprint('core', __name__)

@core.route('/')
def home():
    return render_template('home.html')

@core.route('/about')
def about():
    return render_template('about.html')
