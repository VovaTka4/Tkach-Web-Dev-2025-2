import pytest, re

def test_visits_counter(client):
    response = client.get("/visitscounter")
    assert response.status_code == 200
    page_content = response.get_data(as_text=True)
    assert "1" in page_content