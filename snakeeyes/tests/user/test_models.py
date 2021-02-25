from snakeeyes.user.models import User

class TestUserToken:
    """Testing for token generation and verifictaion"""
    def test_count_token(self, token):
        """ Count the period in the token generated in JWS correctly. """
        assert token.count('.') == 2


    def test_confirm_token(self, token):
        """Recover the email email in dump in the token """
        user = User.query.filter_by(email = 'admin@local.host').first()
        assert user.verify_token(token) == 1

    def test_confirm_reset_token(self,token_reset):
        user = User.confirm_reset_token(token_reset)
        assert user == 1
        
    def test_fail_token(self, token):
        user = User.query.filter_by(email = 'admin@local.host').first()
        u = user.verify_token("{0}123".format(token))
        assert u is False
