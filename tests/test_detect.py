import requests


def test_get_missing_pnrs():
    url = 'http://localhost:5000/detect'
    
    payload = {
        'PNR1': 'AAAAAA', 
        'PNR2': 'AAAAAD'
    }
    
    resp = requests.post(url, json=payload) 
    
    assert resp.status_code == 200
    resp_body = resp.json()
    assert resp_body['Missing PNR-s'] == [
        "AAAAAB",
        "AAAAAC"
    ]


def test_get_missing_pnrs_missing_parameter():
    url = 'http://localhost:5000/detect'
    
    payload = {
        'PNR1': 'AAAAAA', 
    }
    
    resp = requests.post(url, json=payload) 
    
    assert resp.status_code == 200
    resp_body = resp.json()
    assert resp_body['status'] == 301


def test_get_missing_pnrs_wrong_length():
    url = 'http://localhost:5000/detect'
    
    payload = {
        'PNR1': 'AAAAAA', 
        'PNR2': 'AAD'
    }
    
    resp = requests.post(url, json=payload) 
    
    assert resp.status_code == 200
    resp_body = resp.json()
    assert resp_body['status'] == 302


def test_get_missing_pnrs_wrong_symbol():
    url = 'http://localhost:5000/detect'
    
    payload = {
        'PNR1': 'AAAAAA', 
        'PNR2': 'AAAAA.'
    }
    
    resp = requests.post(url, json=payload) 
    
    assert resp.status_code == 200
    resp_body = resp.json()
    assert resp_body['status'] == 303
