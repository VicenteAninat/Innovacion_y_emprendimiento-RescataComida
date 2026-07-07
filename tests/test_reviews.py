import pytest
from unittest.mock import patch
from app.entity.ReviewsEntity import ReviewsEntity

def test_create_review_success(client, mock_user_profile):
    payload = {
        "reservation_id": 12,
        "rating": 5,
        "comment": "Excelente atención y productos!"
    }
    
    mock_review = ReviewsEntity(
        id=1,
        user_id=mock_user_profile.id,
        business_id=5,
        reservation_id=12,
        rating=5,
        comment="Excelente atención y productos!"
    )
    
    with patch("app.controller.ReviewsController.reviews_service.create_review") as mock_create:
        mock_create.return_value = mock_review
        
        response = client.post("/reviews/create", json=payload)
        
        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["rating"] == 5
        mock_create.assert_called_once_with(
            user_id=mock_user_profile.id,
            reservation_id=12,
            rating=5,
            comment="Excelente atención y productos!"
        )

def test_create_review_validation_error(client):
    # Rating debe ser entre 1 y 5 (Pydantic Field validation)
    payload = {
        "reservation_id": 12,
        "rating": 6,
        "comment": "Muy malo"
    }
    
    response = client.post("/reviews/create", json=payload)
    assert response.status_code == 422  # Unprocessable Entity (Pydantic validation error)

def test_update_review_success(client, mock_user_profile):
    payload = {
        "rating": 4,
        "comment": "Actualizado: Estuvo bastante bien."
    }
    
    mock_updated_review = ReviewsEntity(
        id=1,
        user_id=mock_user_profile.id,
        business_id=5,
        reservation_id=12,
        rating=4,
        comment="Actualizado: Estuvo bastante bien."
    )
    
    with patch("app.controller.ReviewsController.reviews_service.update_review") as mock_update:
        mock_update.return_value = mock_updated_review
        
        response = client.patch("/reviews/update/1", json=payload)
        
        assert response.status_code == 200
        assert response.json()["rating"] == 4
        mock_update.assert_called_once_with(
            user_id=mock_user_profile.id,
            review_id=1,
            data=payload
        )

def test_delete_review_success(client, mock_user_profile):
    with patch("app.controller.ReviewsController.reviews_service.delete_review") as mock_delete:
        mock_delete.return_value = True
        
        response = client.delete("/reviews/delete/1")
        
        assert response.status_code == 200
        assert response.json() is True
        mock_delete.assert_called_once_with(
            user_id=mock_user_profile.id,
            review_id=1
        )

def test_get_business_reviews(client):
    mock_reviews = [
        ReviewsEntity(id=1, user_id="user-1", business_id=5, reservation_id=10, rating=4, comment="Bueno")
    ]
    with patch("app.controller.ReviewsController.reviews_service.get_reviews_by_business") as mock_get_by_biz:
        mock_get_by_biz.return_value = mock_reviews
        
        response = client.get("/reviews/business/5")
        
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["id"] == 1
        mock_get_by_biz.assert_called_once_with(5)
