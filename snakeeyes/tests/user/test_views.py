from flask import url_for
from snakeeyes.blueprints.user.models import User
from lib.tests import ViewMixin

class TestLogin(ViewMixin):
    def test_login_page(self):
        response = self.client.get(url_for('user.login'))

        assert response.status_code == 200


    def test_login(self):
        response = self.login()
        assert response.status_code ==  200
        assert 'Log in successful' in str(response.data)


    def test_login_activity(self):
        user = User.query.filter_by(email = 'admin@local.host').first()

        old_sign_in = user.sign_in_count

        response = self.login()

        new_sign_in = user.sign_in_count

        assert response.status_code == 200
        assert (old_sign_in + 1)  == new_sign_in


    def test_fail_login(self):
        response = self.login(email = 'lohhy.ssd@lom')

        assert 'You need to register in order to access this page' in str(response.data)


    def test_inactive_account_login(self):
        response = self.login(email = 'disabled@local.host')

        assert response.status_code == 200
  

    def logout(self):
        assert self.login().status_code == 200
        assert 'successful' in str(self.login().data)
        response = self.logout()
        assert response.status_code == 200
        assert 'You are logged out' in str(response.data)


    def test_logout(self):
        self.login()
        response = self.client.get(url_for('user.logout'), follow_redirects = True)

        assert response.status_code == 200
        assert 'You' in str(response.data)
        

class TestPasswordReset(ViewMixin):
    def test_begin_password_reset(self):
        response = self.client.get(url_for('user.requestpasswordreset'), follow_redirects = True)

        assert response.status_code == 200
        assert 'Password ' not in str(response.data)


    def test_begin_password_as_logded_in(self):
        self.login()

        response = self.client.get(url_for('user.requestpasswordreset'), follow_redirects = False)

        assert response.status_code == 302


    def test_bgin_password_reset_fail(self):
        """Begin reset failure due to non existing account"""
        user = {
            'email ' : 'hello@lloo.lol'
        }

        response = self.client.post(url_for('user.requestpasswordreset'), data = user, follow_redirects = True)

        assert response.status_code == 200
        

    def test_begin_password_reset_successfully(self):
        """Begin password reset succesfully for exixting user"""
        user = {
            'email' : 'admin@local.host'
        }

        response = self.client.post(url_for('user.requestpasswordreset'), data = user , follow_redirects =- True)

        assert response.status_code == 200
        assert 'Password reset link had been sent to your email' in str(response.data)


class TestSignup(ViewMixin):
    def test_sign_up(self):
        """Test registering new user"""
        user = {
            'email' : 'new@account.com',
            'password' : 'password'
        }

        response = self.client.post(url_for('user.register') , data = user, follow_redirects = True )

        assert response.status_code == 200 


class TestViewSettings(ViewMixin):
    def test_settins_page(self):
        self.login()
        response = self.client.get(url_for('user.settings'))

        assert response.status_code == 200