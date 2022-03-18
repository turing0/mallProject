import pytest
from rest_framework.authtoken.models import Token
from mall.models import User

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def get_or_create_token(db, create_user):
    # user = create_user()
    user = User.objects.create(username='123456', password='123456')
    token, _ = Token.objects.get_or_create(user=user)
    return token
