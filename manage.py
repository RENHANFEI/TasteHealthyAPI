#!/usr/bin/env python
import os
from app import create_app, db
# from app.models import BmiGoal
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
	return dict(app=app, db=db)
	
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def deploy():
	'''run deployment tasks'''
	from flask_migrate import upgrade
	from app.models import *

	# upgrade()


if __name__ == '__main__':
	manager.run()

