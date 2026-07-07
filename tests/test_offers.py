import pytest
from unittest.mock import patch
from datetime import datetime
from app.entity.OffersEntity import OffersEntity
from app.controller.AuthController import get_current_user_profile

def test_create_offer_as_customer_forbidden(client):
    payload = {
        "business_id": 1,
        "title": "Bolsa Sorpresa",
        "original_price": 10000.0,
        "discounted_price": 3000.0,
        "pickup_start_time": "2026-07-07T18:00:00",
        "pickup_end_time": "2026-07-07T20:00:00"
    }
    
    # Por defecto, client tiene rol 'customer' (inyectado en conftest.py)
    response = client.post("/offers/create", json=payload)
    assert response.status_code == 403
    assert "Forbidden" in response.json()["detail"]

def test_create_offer_as_worker_success(client, mock_worker_profile):
    # Sobrescribimos perfil con el de un trabajador del negocio 1
    from app.main import app
    app.dependency_overrides[get_current_user_profile] = lambda: mock_worker_profile
    
    payload = {
        "business_id": 1,
        "title": "Bolsa Sorpresa Pastelería",
        "description": "Exquisitos pasteles del día",
        "original_price": 10000.0,
        "discounted_price": 3000.0,
        "quantity_available": 3,
        "pickup_start_time": "2026-07-07T18:00:00",
        "pickup_end_time": "2026-07-07T20:00:00",
        "status": "active",
        "kg_saved_per_unit": 2.0,
        "co2_avoided_per_unit": 5.0
    }
    
    mock_offer = OffersEntity(
        id=10,
        business_id=1,
        title="Bolsa Sorpresa Pastelería",
        description="Exquisitos pasteles del día",
        original_price=10000.0,
        discounted_price=3000.0,
        quantity_available=3,
        pickup_start_time=datetime.fromisoformat("2026-07-07T18:00:00"),
        pickup_end_time=datetime.fromisoformat("2026-07-07T20:00:00"),
        status="active",
        kg_saved_per_unit=2.0,
        co2_avoided_per_unit=5.0
    )
    
    with patch("app.controller.OffersController.offers_service.create_offer") as mock_create:
        mock_create.return_value = mock_offer
        
        response = client.post("/offers/create", json=payload)
        
        assert response.status_code == 200
        assert response.json()["title"] == "Bolsa Sorpresa Pastelería"
        assert response.json()["id"] == 10
        mock_create.assert_called_once()

def test_create_offer_as_worker_wrong_business(client, mock_worker_profile):
    from app.main import app
    app.dependency_overrides[get_current_user_profile] = lambda: mock_worker_profile
    
    # El worker pertenece al business_id=1, pero intenta crear en business_id=2
    payload = {
        "business_id": 2,
        "title": "Bolsa Sorpresa Pastelería",
        "original_price": 10000.0,
        "discounted_price": 3000.0,
        "pickup_start_time": "2026-07-07T18:00:00",
        "pickup_end_time": "2026-07-07T20:00:00"
    }
    
    response = client.post("/offers/create", json=payload)
    assert response.status_code == 403
    assert "No tienes permiso para crear ofertas para un comercio diferente" in response.json()["detail"]

def test_get_all_offers(client):
    mock_offers = [
        OffersEntity(id=1, business_id=1, title="Bolsa 1", original_price=5000, discounted_price=1500, pickup_start_time=datetime.now(), pickup_end_time=datetime.now(), status="active"),
        OffersEntity(id=2, business_id=2, title="Bolsa 2", original_price=6000, discounted_price=2000, pickup_start_time=datetime.now(), pickup_end_time=datetime.now(), status="active")
    ]
    
    with patch("app.controller.OffersController.offers_service.get_all_offers") as mock_get_all:
        mock_get_all.return_value = mock_offers
        
        response = client.get("/offers/get_all")
        
        assert response.status_code == 200
        assert len(response.json()) == 2
        mock_get_all.assert_called_once()

def test_get_offer_by_id_not_found(client):
    with patch("app.controller.OffersController.offers_service.get_offer_by_id") as mock_get_by_id:
        mock_get_by_id.return_value = None
        
        response = client.get("/offers/get/999")
        assert response.status_code == 404
        assert "Oferta no encontrada" in response.json()["detail"]

def test_update_offer_worker_success(client, mock_worker_profile):
    from app.main import app
    app.dependency_overrides[get_current_user_profile] = lambda: mock_worker_profile
    
    # La oferta pertenece al business_id=1
    existing_offer = OffersEntity(
        id=10, business_id=1, title="Original Title", original_price=5000, discounted_price=1500,
        pickup_start_time=datetime.now(), pickup_end_time=datetime.now(), status="active"
    )
    
    updated_offer = OffersEntity(
        id=10, business_id=1, title="Updated Title", original_price=5000, discounted_price=1500,
        pickup_start_time=datetime.now(), pickup_end_time=datetime.now(), status="active"
    )
    
    with patch("app.controller.OffersController.offers_service.get_offer_by_id") as mock_get, \
         patch("app.controller.OffersController.offers_service.update_offer") as mock_update:
        mock_get.return_value = existing_offer
        mock_update.return_value = updated_offer
        
        payload = {"title": "Updated Title"}
        response = client.patch("/offers/update/10", json=payload)
        
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Title"
        mock_get.assert_called_once_with(10)
        mock_update.assert_called_once()

def test_delete_offer_worker_wrong_business(client, mock_worker_profile):
    from app.main import app
    app.dependency_overrides[get_current_user_profile] = lambda: mock_worker_profile
    
    # La oferta pertenece a business_id=2, el worker a business_id=1
    existing_offer = OffersEntity(
        id=10, business_id=2, title="Bolsa", original_price=5000, discounted_price=1500,
        pickup_start_time=datetime.now(), pickup_end_time=datetime.now(), status="active"
    )
    
    with patch("app.controller.OffersController.offers_service.get_offer_by_id") as mock_get:
        mock_get.return_value = existing_offer
        
        response = client.delete("/offers/delete/10")
        assert response.status_code == 403
        assert "No tienes permiso para eliminar ofertas de este comercio" in response.json()["detail"]

def test_get_by_business(client):
    with patch("app.controller.OffersController.offers_service.offers_by_business") as mock_by_business:
        mock_by_business.return_value = []
        
        response = client.get("/offers/business/1")
        assert response.status_code == 200
        assert response.json() == []
        mock_by_business.assert_called_once_with(1)

def test_get_favorite_nearby_offers(client, mock_user_profile):
    with patch("app.controller.OffersController.offers_service.get_favorite_businesses_offers_nearby") as mock_fav_offers:
        mock_fav_offers.return_value = []
        
        response = client.get("/offers/favorite-nearby?lat=-33.4&lng=-70.6&radius_km=5")
        assert response.status_code == 200
        assert response.json() == []
        mock_fav_offers.assert_called_once_with(mock_user_profile.id, -33.4, -70.6, 5.0)

def test_get_active_offers_by_business(client):
    with patch("app.controller.OffersController.offers_service.get_active_offers_by_business") as mock_active:
        mock_active.return_value = []
        
        response = client.get("/offers/active/1")
        assert response.status_code == 200
        assert response.json() == []
        mock_active.assert_called_once_with(1)

def test_get_global_active_offers_no_location(client):
    with patch("app.controller.OffersController.offers_service.get_active_offers") as mock_get_active:
        mock_get_active.return_value = []
        
        response = client.get("/offers/active?limit=15&offset=5")
        assert response.status_code == 200
        assert response.json() == []
        mock_get_active.assert_called_once_with(None, None, 5.0, 15, 5)

def test_get_global_active_offers_with_location(client):
    with patch("app.controller.OffersController.offers_service.get_active_offers") as mock_get_active:
        mock_get_active.return_value = []
        
        response = client.get("/offers/active?lat=-33.45&lng=-70.62&radius_km=8&limit=5&offset=0")
        assert response.status_code == 200
        assert response.json() == []
        mock_get_active.assert_called_once_with(-33.45, -70.62, 8.0, 5, 0)

def test_service_get_active_offers_logic():
    from app.service.OffersService import OffersService
    service = OffersService()
    
    with patch.object(service.offers_repository, "get_active_offers_nearby") as mock_nearby, \
         patch.object(service.offers_repository, "get_active_offers_paginated") as mock_paginated:
         
        # Caso 1: con ubicación
        mock_nearby.return_value = []
        res = service.get_active_offers(lat=-33.45, lng=-70.62, radius_km=10.0, limit=10, offset=0)
        assert res == []
        mock_nearby.assert_called_once_with(-33.45, -70.62, 10.0, 10, 0)
        mock_paginated.assert_not_called()
        
        # Caso 2: sin ubicación
        mock_nearby.reset_mock()
        mock_paginated.return_value = []
        res_pag = service.get_active_offers(lat=None, lng=None, radius_km=5.0, limit=20, offset=10)
        assert res_pag == []
        mock_paginated.assert_called_once_with(20, 10)
        mock_nearby.assert_not_called()
