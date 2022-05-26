from flask.testing import FlaskClient
import pytest
from werkzeug.test import TestResponse
from movies.entrypoints.flask_app import app
from movies.sql_alchemy_repository import SqlAlchemyRepository

@pytest.fixture
def db():
    return SqlAlchemyRepository()

@pytest.fixture
def client(db: SqlAlchemyRepository):
    db.re_populate_movies()
    yield app.test_client()
    db.drop_all()

def create_emifervi(client: FlaskClient):
    args = 'username=emifervi&email=emifervi@gmail.com'
    preferences = 'preferences=1&preferences=2&preferences=3'
    return client.post(
        f'/create_user?{args}&{preferences}',
    )

def test_create_user(client: FlaskClient):
    response = create_emifervi(client)
    json_response = response.json
    assert response.status_code == 200
    assert json_response is not None
    assert json_response['message'] == 'User created succesfully!'
    assert 'user' in json_response

def assert_missing(response: TestResponse, expected_message: str):
    json_response = response.json
    assert response.status_code == 400
    assert json_response is not None
    assert json_response['message'] == expected_message
    assert 'user' not in json_response

def test_create_user_missing(client: FlaskClient):
    assert_missing(client.post('/create_user'), 'No username provided!')
    with_username = 'username=jalvito'
    assert_missing(
        client.post(f'/create_user?{with_username}'),
        'No email provided!'
    )
    with_email = f'{with_username}&email=jalvito@google.com'
    assert_missing(
        client.post(f'/create_user?{with_email}'),
        'No preferences provided!'
    )
    with_less_prefs = with_email
    for i in range(1, 3):
        with_less_prefs += f'&preferences={i}'
        assert_missing(
            client.post(f'/create_user?{with_less_prefs}'),
            '3 preferences must be selected!'
        )
    with_more_prefs = f'{with_less_prefs}&preferences=3&preferences=4'
    assert_missing(
        client.post(f'/create_user?{with_more_prefs}'),
        '3 preferences must be selected!'
    )

def test_create_user_duplicate(client: FlaskClient):
    create_emifervi(client)
    response = create_emifervi(client)
    json_response = response.json
    assert response.status_code == 409
    assert json_response is not None
    assert json_response['message'] == 'User already exists!'
    assert 'user' not in json_response