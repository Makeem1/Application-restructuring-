from flask import render_template, url_for, flash, redirect

from snakeeyes.contact import contact

@contact.route('/contact', methods=['GET', 'POST'])
def index():
    form = ContactForm()

    if form.validate_on_submit():
        flash("You will get a response soon")
        return redirect(url_for('contact.index'))

    return render_template('index.html', form = form )