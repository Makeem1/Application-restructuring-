from flask import url_for
from snakeeyes.user.models import User
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
        assert 'Your account has been temporary disable, please visit support for assisstance' in str(response.data)


    def test_logout(self):
        response = self.client.get(url_for('user.logout'), follow_redirects = True)

        assert response.status_code == 200
        

class TestPasswordReset(ViewMixin):
    def test_begin_password_reset(self):
        response = self.client.get(url_for('user.requestpasswordreset'))

        assert response.status_code == 200


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

    def test_unconfirmed_login_user(self):
        """Test to verify that unconfirmed user are directed to a unconfirmed page"""
        self.login()
        response = self.client.get(url_for('user.unconfirmed'), follow_redirects = False)

        assert response.status_code == 200
