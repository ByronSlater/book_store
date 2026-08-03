
def test_authors_response_status(seed_db, test_client):
    response = test_client.get('/authors')

    assert response.status_code == 200


def test_author_response_body(seed_db, test_client):
    response = test_client.get('/authors')

    assert response.json == [
        {
            "name": "Julia Donaldson",
            "dob": "1948-09-16"
        },
        {
            "name": "Andrea Beaty",
            "dob": "1961-10-08"
        },
        {
            "name": "Kelly Barnhill",
            "dob": "1973-01-01"
        },
        {
            "name": "Zetta Elliott",
            "dob": "1979-11-11"
        }
    ]
