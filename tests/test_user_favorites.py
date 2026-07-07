import pytest
from unittest.mock import patch
from app.entity.UserFavoritesEntity import UserFavoritesEntity
from app.entity.BusinessesEntity import BusinessesEntity

def test_add_favorite_success(client, mock_user_profile):
    mock_favorite = UserFavoritesEntity(
        id=1,
        user_id=mock_user_profile.id,
        business_id=5
    )
    
    with patch("app.controller.UserFavoritesController.favorites_service.add_favorite") as mock_add:
        mock_add.return_value = mock_favorite
        
        response = client.post("/favorites/add/5")
        
        assert response.status_code == 200
        assert response.json()["business_id"] == 5
        assert response.json()["user_id"] == mock_user_profile.id
        mock_add.assert_called_once_with(mock_user_profile.id, 5)

def test_remove_favorite_success(client, mock_user_profile):
    with patch("app.controller.UserFavoritesController.favorites_service.remove_favorite") as mock_remove:
        mock_remove.return_value = True
        
        response = client.delete("/favorites/remove/5")
        
        assert response.status_code == 200
        assert response.json() is True
        mock_remove.assert_called_once_with(mock_user_profile.id, 5)

def test_check_favorite_true(client, mock_user_profile):
    with patch("app.controller.UserFavoritesController.favorites_service.is_favorite") as mock_check:
        mock_check.return_value = True
        
        response = client.get("/favorites/check/5")
        
        assert response.status_code == 200
        assert response.json() is True
        mock_check.assert_called_once_with(mock_user_profile.id, 5)

def test_get_my_favorites(client, mock_user_profile):
    mock_favorites = [
        BusinessesEntity(id=5, rut="11111111-1", name="Cafe Central", category="Cafe", address="Paseo Ahumada", location="POINT(-70.6 33.4)")
    ]
    
    with patch("app.controller.UserFavoritesController.favorites_service.get_favorites_by_user") as mock_get:
        mock_get.return_value = mock_favorites
        
        response = client.get("/favorites/my-favorites")
        
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["name"] == "Cafe Central"
        mock_get.assert_called_once_with(mock_user_profile.id)
