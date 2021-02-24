from flask import url_for

class TestContact:
    """This is a class function for testing contact page"""
    def test_contact_page(self, client):
        response = client.get(url_for('contact.index'))
        assert response.status_code == 200

    def test_contact_me(self,client):
        """Testing contact me""" 
        response = client.post(url_for('contact.index'), data=dict(
        email='hello@gmail.com',
        message = 'Hello world, it is cool here'), follow_redirects=True)

        assert response.status_code == 200
        assert message in str(response.data)