import pytest
from movies.entrypoints.flask_app import app
from movies.sql_alchemy_repository import SqlAlchemyRepository

@pytest.fixture
def db():
    return SqlAlchemyRepository()

@pytest.fixture
def app_fixture(db):
    app.config.from_object('project.config.TestingConfig')
    with app.app_context():   
        db.create_all()
        return app
