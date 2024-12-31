import requests

def test_app_is_running():
    response = requests.get("http://app:5000")
    assert response.status_code == 200
