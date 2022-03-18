import pytest


@pytest.mark.django_db
def test_unauthorized_request(api_client):
    response = api_client.get('/api/products')
    assert response.status_code == 301


@pytest.mark.django_db
def test_unauthorized_request2(api_client):
    response = api_client.get('/api/orders')
    assert response.status_code == 301


@pytest.mark.django_db
def test_404_request(api_client):
    response = api_client.get('/api/xxx')
    assert response.status_code == 404


# @pytest.mark.django_db
# def test_unauthorized_request(api_client, get_or_create_token):
#    token = get_or_create_token()
#    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
#    response = api_client.get('/api/products')
#    assert response.status_code == 200

# @pytest.mark.django_db
# def test_register(api_client):
#     response = api_client.post('/api/register')
#     assert response.status_code == 404

# def test_unauthorized_request(api_client):
#     response = api_client.post('/api/products/buy')
#     assert response.status_code == 301
