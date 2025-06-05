import pytest
from app import app

def test_homepage():
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://powerplay_assistant:elite.niceygy.net@10.0.0.52/elite"
    app.config['TEST'] = True
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.text.__contains__("PPA: All Operational")
        assert response.headers.__contains__("X-Powered-By")
        
def test_404():
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://powerplay_assistant:elite.niceygy.net@10.0.0.52/elite"
    with app.test_client() as client:
        response = client.get("/404")
        assert response.status_code == 404
        assert response.text.__contains__('umami.track("error_404");')

def test_system_search():
    # app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://powerplay_assistant:elite.niceygy.net@10.0.0.52/elite"
    with app.test_client() as client:
        response = client.get("/search_systems?query=Sol")
        assert response.status_code == 200
        assert response.text.__contains__("Sol")