# services/users/manage.py


import coverage
import unittest
import xmlrunner

from flask.cli import FlaskGroup  # to allow command line interaction

from project import create_app, db
from project.api.models import User


COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py',
    ]
)
COV.start()

app = create_app()


# we created a new FlaskGroup instance to extend the normal CLI
# #with commands related to the Flask app.
cli = FlaskGroup(create_app=create_app)


'''This registers a new command, recreate_db, to the CLI
so that we can run it from the command line,
 which we’ll use shortly to apply the model to the database.'''


@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


#  to discover and run the tests:
@cli.command()
def test():
    """ Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    test_result = xmlrunner.XMLTestRunner(output="xml_test_result", verbosity=2
                                          ).run(unittest.TestLoader().
                                                discover('project/tests'))
    # tests = unittest.TestLoader().discover('project/tests')
    # result = unittest.TextTestRunner(verbosity=2).run(tests)
    '''"sudo docker-compose -f docker-compose-dev.yml
    run users flake8 --max-complexity 12 project
    --output-file flake8-output.txt || exit 0" use
    this command to generate flake8 result'''
    if test_result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.xml_report()
        # COV.erase()
        return 0
    return 1


@cli.command()
def seed_db():
    """Seeds the database."""
    db.session.add(User(username='msitdevops', email="msitdevops@gmail.com",
                        password='greaterthaneight'))
    db.session.add(User(username='teamdevops', email="teamdevops@gmail.com",
                        password='greaterthaneight'))
    db.session.commit()


if __name__ == '__main__':
    cli()
