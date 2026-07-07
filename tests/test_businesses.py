import pytest
from unittest.mock import patch
from app.entity.BusinessesEntity import BusinessesEntity

def test_create_business_success(client):
    payload = {
        "rut": "12345678-9",
        "name": "Panadería Super",
        "category": "Panadería",
        "address": "Av Costanera 100",
        "location": "POINT(-70.6 33.4)"
    }
    
    mock_business = BusinessesEntity(
        id=1,
        rut="12345678-9",
        name="Panadería Super",
        category="Panadería",
        address="Av Costanera 100",
        location="POINT(-70.6 33.4)"
    )
    
    with patch("app.controller.BusinessesController.business_service.create_businesses") as mock_create:
        mock_create.return_value = mock_business
        
        response = client.post("/businesses/create", json=payload)
        
        assert response.status_code == 200
        assert response.json()["name"] == "Panadería Super"
        assert response.json()["id"] == 1
        mock_create.assert_called_once_with(
            "12345678-9",
            "Panadería Super",
            "Panadería",
            "Av Costanera 100",
            "POINT(-70.6 33.4)"
        )

def test_get_all_businesses(client):
    mock_businesses = [
        BusinessesEntity(id=1, rut="12345678-9", name="Panadería Super", category="Panadería", address="Av Costanera 100", location="POINT(-70.6 33.4)"),
        BusinessesEntity(id=2, rut="98765432-1", name="Verdulería Don Pepito", category="Verdulería", address="Av Siempreviva 742", location="POINT(-70.7 33.5)")
    ]
    
    with patch("app.controller.BusinessesController.business_service.get_all_businesses") as mock_get_all:
        mock_get_all.return_value = mock_businesses
        
        response = client.get("/businesses/get_all")
        
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["name"] == "Panadería Super"
        assert response.json()[1]["name"] == "Verdulería Don Pepito"
        mock_get_all.assert_called_once()

def test_get_business_by_id_success(client):
    mock_business = BusinessesEntity(
        id=5,
        rut="11111111-1",
        name="Local 5",
        category="Cafetería",
        address="Av Italia 50",
        location="POINT(-70.5 33.3)"
    )
    
    with patch("app.controller.BusinessesController.business_service.get_business_by_id") as mock_get_by_id:
        mock_get_by_id.return_value = mock_business
        
        response = client.get("/businesses/get/5")
        
        assert response.status_code == 200
        assert response.json()["name"] == "Local 5"
        mock_get_by_id.assert_called_once_with(5)

def test_update_business_success(client):
    payload = {
        "rut": "11111111-1",
        "name": "Cafetería Italia Actualizada",
        "category": "Cafetería",
        "address": "Av Italia 50",
        "location": "POINT(-70.5 33.3)"
    }
    
    mock_updated_business = BusinessesEntity(
        id=5,
        rut="11111111-1",
        name="Cafetería Italia Actualizada",
        category="Cafetería",
        address="Av Italia 50",
        location="POINT(-70.5 33.3)"
    )
    
    with patch("app.controller.BusinessesController.business_service.update_businesses") as mock_update:
        mock_update.return_value = mock_updated_business
        
        # El endpoint recibe business_id por query string y el payload en el body
        response = client.patch("/businesses/update?business_id=5", json=payload)
        
        assert response.status_code == 200
        assert response.json()["name"] == "Cafetería Italia Actualizada"
        # Notar que data.dict(exclude_unset=True) en el controlador enviará todas las llaves del payload
        mock_update.assert_called_once_with("5", payload)

def test_delete_business_success(client):
    with patch("app.controller.BusinessesController.business_service.delete_businesses") as mock_delete:
        mock_delete.return_value = 1
        
        response = client.post("/businesses/delete/5")
        
        assert response.status_code == 200
        assert response.json() == 1
        mock_delete.assert_called_once_with("5")

def test_get_nearby_with_offers(client):
    mock_businesses = [
        BusinessesEntity(id=1, rut="12345678-9", name="Panadería Super", category="Panadería", address="Av Costanera 100", location="POINT(-70.6 33.4)"),
    ]
    
    with patch("app.controller.BusinessesController.business_service.get_nearby_businesses_with_active_offers") as mock_nearby:
        mock_nearby.return_value = mock_businesses
        
        response = client.get("/businesses/nearby-with-offers?lat=-33.4&lng=-70.6&radius_km=5.0")
        
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["id"] == 1
        mock_nearby.assert_called_once_with(-33.4, -70.6, 5.0)

def test_get_favorite_nearby(client, mock_user_profile):
    mock_businesses = [
        BusinessesEntity(id=2, rut="98765432-1", name="Verdulería Don Pepito", category="Verdulería", address="Av Siempreviva 742", location="POINT(-70.7 33.5)")
    ]
    
    with patch("app.controller.BusinessesController.business_service.get_favorite_businesses_with_active_offers_nearby") as mock_fav_nearby:
        mock_fav_nearby.return_value = mock_businesses
        
        response = client.get("/businesses/favorite-nearby?lat=-33.5&lng=-70.7&radius_km=5.0")
        
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["id"] == 2
        mock_fav_nearby.assert_called_once_with(mock_user_profile.id, -33.5, -70.7, 5.0)
