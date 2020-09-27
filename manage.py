from app import create_app
from flask_script import Manager, Server
from app import db
from app.models import User, BlogPost, Image, Comment
from flask_migrate import Migrate, MigrateCommand

# import the create app funtion from app and create an instance of the entire app while passing in the cofiguration settings in the parameters of the funtion
app = create_app('production')

manager = Manager(app)
migrate = Migrate(app, db)

# add command for running the server using manager
manager.add_command('server', Server)
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User, BlogPost=BlogPost, Image=Image, Comment=Comment)


if __name__ == '__main__':
    manager.run()