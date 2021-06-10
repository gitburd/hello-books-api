from app.models.book import Book


def test_get_all_books_with_no_records(client):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_book_with_valid_id(client, two_saved_books):
    # Act
    response = client.get("/books/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body['book'] == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }


def test_get_book_with_invalid_id(client):
    # Act
    response = client.get("/books/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == None


def test_post_planet(client):
    response = client.post("/books/", json={
        "title": "Ocean Book",
        "description": "watr 4evr"
    })

    assert response.status_code == 201
