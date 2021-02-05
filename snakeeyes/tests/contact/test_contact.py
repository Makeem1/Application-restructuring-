from flask import url_for

class TestContact:
    """This is a class function for testing contact page"""
    def test_contact(self, client):
        response = client.get(url_for('contact.index'))
        assert response.status_code == 200
        