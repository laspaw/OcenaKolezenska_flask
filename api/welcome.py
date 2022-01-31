from flask import render_template


def welcome():
    return render_template('endpoints/welcome.html.jinja2')
