import csv
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_csv():
    with open('top_insta_influencers_data.csv', mode='r') as file:
        reader = csv.reader(file)
        data = list(reader)
        assert len(data) > 0  # Example assertion


def test_read_main():
    response = client.get("/filter?min_influence_score=85")
    assert response.status_code == 200
    assert all(
        influencer['influence_score'] is None or influencer['influence_score'] >= 85 for influencer in response.json())

    response = client.get("/filter?min_followers=1000000")
    assert response.status_code == 200
    assert all(influencer['followers_numeric'] is None or influencer['followers_numeric'] >= 1000000 for influencer in
               response.json())

    response = client.get("/filter?country=India")
    assert response.status_code == 200
    assert all(influencer['country'] == 'India' for influencer in response.json())

    response = client.get("/filter?min_avg_likes=8200000")
    assert response.status_code == 200
    assert all(influencer['average_numeric'] is None or influencer['average_numeric'] >= 8200000 for influencer in
               response.json())
