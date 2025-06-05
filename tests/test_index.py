import pytest
from app import app

def test_homepage():
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.text.__contains__("PPA: All Operational")
        assert response.headers.__contains__("X-Powered-By")
        
def test_404():
    with app.test_client() as client:
        response = client.get("/404")
        assert response.status_code == 404
        assert response.text.__contains__('umami.track("error_404");')

def test_system_search():
    with app.test_client() as client:
        response = client.get("/search_systems?query=Sol")
        assert response.status_code == 200
        assert response.text.__contains__("Sol")
        
def test_megaships():
    with app.test_client() as client:
        response = client.get("/results?system=Sol&power=Jerome+Archer&taskName=Scan+Megaship+Datalinks&choice=Reinforce")
        assert response.status_code == 200
        assert response.text.__contains__("Found 15 megaships in Jerome")