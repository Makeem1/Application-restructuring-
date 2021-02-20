from snakeeyes import create_app
from flask_script import Manager, Shell
from snakeeyes.user.models import User
from snakeeyes.extensions import db



app = create_app()
manager = Manager(app)

def make_shell_context():
    return dict(app=app, User=User, db=db )
manager.add_command('shell', Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()


