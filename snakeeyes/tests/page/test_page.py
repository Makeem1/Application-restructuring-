from flask import url_for


class TestPage:
    '''Test class for the static pages'''
    
    def test_home(self, client):
        """Test for if the response code is 200, whcih means it pa"""
        response = client.get(url_for('page.home'))
        assert response.status_code == 200

    def test_privacy(self, client):
        response = client.get(url_for('page.privacy'))
        assert response.status_code == 200

    def test_questions(self, client):
        response = client.get(url_for('page.questions'))
        assert response.status_code == 200

    def test_terms(self, client):
        response = client.get(url_for('page.terms'))
        assert response.status_code == 200

