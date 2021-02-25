from flask import url_for
from snakeeyes.extensions import mail 
from snakeeyes.email import contact_me

class TestContact:
    """This is a class function for testing contact page"""
    def test_contact_page(self, client):
        response = client.get(url_for('contact.index'))
        assert response.status_code == 200

    def test_contact_me(self,client):
        """Testing contact me""" 
        form = {
          'email': 'foo@bar.com',
          'message': 'Test message from Snake Eyes.'
        }

        response = client.post(url_for('contact.index'), data=form, follow_redirects=True)

        assert response.status_code == 200
        assert "You will get a response soon" in str(response.data)


    def test_deliver_support_email(self):
        """ Deliver a contact email. """
        form = {
          'email': 'foo@bar.com',
          'message': 'Test message from Snake Eyes.'
        }

        with mail.record_messages() as outbox:
            contact_me(form.get('email'), 
                form.get('message'), 'contact', 'contact/mail/index', data = form )

            assert len(outbox) == 1
            assert form.get('email') in outbox[0].body





