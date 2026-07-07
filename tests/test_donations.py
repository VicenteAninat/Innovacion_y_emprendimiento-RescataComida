import pytest
from unittest.mock import patch
from app.entity.DonationsEntity import DonationsEntity

def test_create_donation(client):
    payload = {
        "business_id": 1,
        "food_bank_id": 2,
        "description": "Donación de panadería y bollería",
        "weight_kg": 15.5,
        "tax_deductible_receipt_url": "https://supabase.co/receipt.pdf"
    }
    
    mock_donation = DonationsEntity(
        id=1,
        business_id=1,
        food_bank_id=2,
        description="Donación de panadería y bollería",
        weight_kg=15.5,
        tax_deductible_receipt_url="https://supabase.co/receipt.pdf"
    )
    
    with patch("app.controller.DonationsController.donations_service.create_donation") as mock_create:
        mock_create.return_value = mock_donation
        
        response = client.post("/donations/create", json=payload)
        
        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["weight_kg"] == 15.5
        mock_create.assert_called_once_with(
            business_id=1,
            food_bank_id=2,
            description="Donación de panadería y bollería",
            weight_kg=15.5,
            tax_deductible_receipt_url="https://supabase.co/receipt.pdf"
        )

def test_get_all_donations(client):
    with patch("app.controller.DonationsController.donations_service.get_all_donations") as mock_get_all:
        mock_get_all.return_value = []
        
        response = client.get("/donations/get_all")
        assert response.status_code == 200
        assert response.json() == []
        mock_get_all.assert_called_once()

def test_get_donation_by_id_success(client):
    mock_donation = DonationsEntity(id=3, business_id=1, food_bank_id=2, weight_kg=10)
    with patch("app.controller.DonationsController.donations_service.get_donation_by_id") as mock_get:
        mock_get.return_value = mock_donation
        
        response = client.get("/donations/get/3")
        assert response.status_code == 200
        assert response.json()["id"] == 3
        mock_get.assert_called_once_with(3)

def test_get_donation_by_id_not_found(client):
    with patch("app.controller.DonationsController.donations_service.get_donation_by_id") as mock_get:
        mock_get.return_value = None
        
        response = client.get("/donations/get/99")
        assert response.status_code == 404
        assert "Donación no encontrada" in response.json()["detail"]

def test_get_donations_by_business(client):
    with patch("app.controller.DonationsController.donations_service.get_donations_by_business") as mock_get_by_biz:
        mock_get_by_biz.return_value = []
        
        response = client.get("/donations/business/1")
        assert response.status_code == 200
        assert response.json() == []
        mock_get_by_biz.assert_called_once_with(1)

def test_update_donation(client):
    payload = {"description": "Descripción Actualizada"}
    mock_donation = DonationsEntity(id=3, business_id=1, food_bank_id=2, description="Descripción Actualizada")
    
    with patch("app.controller.DonationsController.donations_service.update_donation") as mock_update:
        mock_update.return_value = mock_donation
        
        response = client.patch("/donations/update/3", json=payload)
        
        assert response.status_code == 200
        assert response.json()["description"] == "Descripción Actualizada"
        mock_update.assert_called_once_with(3, payload)

def test_delete_donation(client):
    with patch("app.controller.DonationsController.donations_service.delete_donation") as mock_delete:
        mock_delete.return_value = True
        
        response = client.post("/donations/delete/3")
        
        assert response.status_code == 200
        assert response.json() is True
        mock_delete.assert_called_once_with(3)
