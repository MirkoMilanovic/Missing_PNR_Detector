import requests

def test_get_missing_pnrs():
    r = requests.get('http://localhost:5000/get')
    assert r.status_code == 200
