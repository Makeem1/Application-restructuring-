from flask import url_for
from snakeeyes.user.models import User
from lib.tests import ViewMixin

class TestLogin(ViewMixin):
    def test_login_page(self):
        response = self.client.get(url_for('user.login'))

        assert response == 200

    def test_login(self):
        response = self.login()

        assert response == 200