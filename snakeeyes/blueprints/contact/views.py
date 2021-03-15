from flask import render_template, url_for, flash, redirect, request



from snakeeyes.blueprints.contact.forms import ContactForm
from flask_login import current_user
from snakeeyes.blueprints.contact import contact
from snakeeyes.email import contact_me 


@contact.route('/contact', methods=['GET', 'POST'])
def index():
    form = ContactForm(obj=current_user)

    if form.validate_on_submit():
        email = form.email.data
        message = form.message.data
        data = {"email" : email, "message" : message}
        
        """import send_email here inorder to prevent circular import of celery app"""
        
        from snakeeyes.email import contact_me

        contact_me(email, message, 'contact', 'contact/mail/index' , data = data)
        flash("You will get a response soon", 'success')
        return redirect(url_for('contact.index'))

    return render_template('contact/index.html', form = form )