from flask import render_template, url_for, flash, redirect, request



from snakeeyes.contact.forms import ContactForm

from snakeeyes.contact import contact
from snakeeyes.contact.task import send_email 


@contact.route('/contact', methods=['GET', 'POST'])
def index():
    form = ContactForm()

    if form.validate_on_submit():
        email = form.email.data
        message = form.message.data
        data = {"email" : email, "message" : message}
        
        """import send_email here inorder to prevent circular import of celery app"""
        
        from snakeeyes.email import send_email

        send_email.delay(email, message, 'contact', 'contact/mail/index' , data = data)
        flash("You will get a response soon", 'success')
        return redirect(url_for('contact.index'))

    return render_template('contact/index.html', form = form )