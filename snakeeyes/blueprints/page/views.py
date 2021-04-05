from flask import render_template

from snakeeyes.blueprints.page import page 

@page.route('/home')
def home():
    return render_template('page/home.html')


@page.route('/privacy')
def privacy():
    return render_template('page/privacy.html')


@page.route('/questions')
def questions():
    return render_template('page/questions.html')


@page.route('/terms')
def terms():
    return render_template('page/terms.html')