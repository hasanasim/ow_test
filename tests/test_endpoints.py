from starlette.testclient import TestClient
from app.main import app


def test_get_titles():
    client = TestClient(app)
    response = client.get('/api/titles/')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    content = response.json()
    assert len(content) == 1000
    first_title = content[0]
    assert first_title['id'] is not None
    assert first_title['title_number'] is not None
    assert first_title['title_class'] is not None
    assert first_title.get('content') is None


def test_get_titles_paging_with_limits():
    client = TestClient(app)
    response = client.get('/api/titles/?_page=1&_limit=10')
    content = response.json()

    assert content
    assert len(content) == 10


def test_get_titles_sorting():
    client = TestClient(app)
    response = client.get('/api/titles/?_sort=id')
    content = response.json()
    assert content
    for i in range(10):
        assert content[i]['id'] == i


def test_get_title_by_id():
    client = TestClient(app)
    title_id = 1
    response = client.get(f'/api/titles/{title_id}')
    content = response.json()
    assert content['id'] == 1
    assert content.get('content') is not None
