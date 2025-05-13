import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.models.users import Base, Users
from dependencies.db import get_session
from main import app


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    Base.metadata.drop_all(engine)



@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override

        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user(session):
    user = Users(
        username='joao',
        email='joao@gmail.com',
        password='234hj45',
        phone_number='35999876765',
        first_name='João',
        last_name='Pedro',
        gender='male'
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def token(client):
    user_data = {
        "username": "joao",
        "email": "joao@gmail.com",
        "password": "234hj45",
        "phone_number": "35999876765",
        "first_name": "João",
        "last_name": "Pedro",
        "gender": "M"
    }
    signup_response = client.post("/signup/", json=user_data)
    assert signup_response.status_code == 201

    login_data = {
        "username": "joao",
        "password": "234hj45"
    }
    login_response = client.post("/login", data=login_data)

    assert login_response.status_code == 200
    return login_response.json()["access_token"]
