import pytest
from unittest.mock import patch
from app.entity.FoodBanksEntity import FoodBanksEntity

def test_create_food_bank(client):
    payload = {
        "rut": "77777777-7",
        "name": "Red de Alimentos",
        "contact_email": "contacto@redalimentos.cl",
        "contact_phone": "+56222222222",
        "address": "Av Santiago 123"
    }
    
    mock_food_bank = FoodBanksEntity(
        id=1,
        rut="77777777-7",
        name="Red de Alimentos",
        contact_email="contacto@redalimentos.cl",
        contact_phone="+56222222222",
        address="Av Santiago 123"
    )
    
    with patch("app.controller.FoodBanksController.food_banks_service.create_food_bank") as mock_create:
        mock_create.return_value = mock_food_bank
        
        response = client.post("/foodbanks/create", json=payload)
        
        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["name"] == "Red de Alimentos"
        mock_create.assert_called_once_with(
            rut="77777777-7",
            name="Red de Alimentos",
            contact_email="contacto@redalimentos.cl",
            contact_phone="+56222222222",
            address="Av Santiago 123"
        )

def test_get_all_food_banks(client):
    with patch("app.controller.FoodBanksController.food_banks_service.get_all_food_banks") as mock_get_all:
        mock_get_all.return_value = []
        
        response = client.get("/foodbanks/get_all")
        assert response.status_code == 200
        assert response.json() == []
        mock_get_all.assert_called_once()

def test_get_food_bank_by_id_success(client):
    mock_fb = FoodBanksEntity(id=3, rut="77777777-7", name="Banco 3")
    with patch("app.controller.FoodBanksController.food_banks_service.get_food_bank_by_id") as mock_get:
        mock_get.return_value = mock_fb
        
        response = client.get("/foodbanks/get/3")
        assert response.status_code == 200
        assert response.json()["id"] == 3
        mock_get.assert_called_once_with(3)

def test_get_food_bank_by_id_not_found(client):
    with patch("app.controller.FoodBanksController.food_banks_service.get_food_bank_by_id") as mock_get:
        mock_get.return_value = None
        
        response = client.get("/foodbanks/get/99")
        assert response.status_code == 404
        assert "Banco de alimentos no encontrado" in response.json()["detail"]

def test_update_food_bank(client):
    payload = {"name": "Nombre Actualizado"}
    mock_fb = FoodBanksEntity(id=3, rut="77777777-7", name="Nombre Actualizado")
    
    with patch("app.controller.FoodBanksController.food_banks_service.update_food_bank") as mock_update:
        mock_update.return_value = mock_fb
        
        response = client.patch("/foodbanks/update/3", json=payload)
        
        assert response.status_code == 200
        assert response.json()["name"] == "Nombre Actualizado"
        mock_update.assert_called_once_with(3, payload)

def test_delete_food_bank(client):
    with patch("app.controller.FoodBanksController.food_banks_service.delete_food_bank") as mock_delete:
        mock_delete.return_value = True
        
        response = client.post("/foodbanks/delete/3")
        
        assert response.status_code == 200
        assert response.json() is True
        mock_delete.assert_called_once_with(3)
