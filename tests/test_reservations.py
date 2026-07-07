import pytest
from unittest.mock import patch
from app.entity.ReservationsEntity import ReservationsEntity

def test_create_reservation_success(client, mock_user_profile):
    payload = {
        "offer_id": 10,
        "quantity": 2,
        "payment_method": "credit_card",
        "transaction_fee": 150.0
    }
    
    mock_reservation = ReservationsEntity(
        id=1,
        user_id=mock_user_profile.id,
        offer_id=10,
        quantity=2,
        total_price=6000.0,
        status="pending",
        payment_method="credit_card",
        transaction_fee=150.0
    )
    
    with patch("app.controller.ReservationsController.reservations_service.create_reservation") as mock_create:
        mock_create.return_value = mock_reservation
        
        response = client.post("/reservations/create", json=payload)
        
        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["total_price"] == 6000.0
        # Validar los argumentos que recibe create_reservation
        mock_create.assert_called_once()
        called_arg = mock_create.call_args[0][0]
        assert called_arg.user_id == mock_user_profile.id
        assert called_arg.offer_id == 10
        assert called_arg.quantity == 2
        assert called_arg.payment_method == "credit_card"

def test_create_reservation_value_error(client):
    payload = {
        "offer_id": 10,
        "quantity": -1
    }
    
    with patch("app.controller.ReservationsController.reservations_service.create_reservation") as mock_create:
        mock_create.side_effect = ValueError("La cantidad debe ser mayor que cero")
        
        response = client.post("/reservations/create", json=payload)
        
        assert response.status_code == 400
        assert "La cantidad debe ser mayor que cero" in response.json()["detail"]

def test_get_my_reservations(client, mock_user_profile):
    mock_res_list = [
        ReservationsEntity(id=1, user_id=mock_user_profile.id, offer_id=10, quantity=2, total_price=6000.0, status="pending")
    ]
    
    with patch("app.controller.ReservationsController.reservations_service.get_reservations_by_user_id") as mock_get:
        mock_get.return_value = mock_res_list
        
        response = client.get("/reservations/my-reservations")
        
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["id"] == 1
        mock_get.assert_called_once_with(mock_user_profile.id)

def test_get_all_reservations(client):
    with patch("app.controller.ReservationsController.reservations_service.get_all_reservations") as mock_get_all:
        mock_get_all.return_value = []
        
        response = client.get("/reservations/get_all")
        assert response.status_code == 200
        assert response.json() == []
        mock_get_all.assert_called_once()

def test_get_reservation_by_id_success(client):
    mock_res = ReservationsEntity(id=1, user_id="some-user", offer_id=10, quantity=2, total_price=6000.0, status="pending")
    with patch("app.controller.ReservationsController.reservations_service.get_reservation_by_id") as mock_get_by_id:
        mock_get_by_id.return_value = mock_res
        
        response = client.get("/reservations/get/1")
        assert response.status_code == 200
        assert response.json()["id"] == 1
        mock_get_by_id.assert_called_once_with(1)

def test_get_reservation_by_id_not_found(client):
    with patch("app.controller.ReservationsController.reservations_service.get_reservation_by_id") as mock_get_by_id:
        mock_get_by_id.return_value = None
        
        response = client.get("/reservations/get/99")
        assert response.status_code == 404
        assert "Reserva no encontrada" in response.json()["detail"]

def test_update_reservation(client):
    payload = {
        "status": "paid",
        "payment_method": "paypal"
    }
    
    mock_res = ReservationsEntity(id=1, user_id="some-user", offer_id=10, quantity=2, total_price=6000.0, status="paid", payment_method="paypal")
    
    with patch("app.controller.ReservationsController.reservations_service.update_reservation") as mock_update:
        mock_update.return_value = mock_res
        
        response = client.patch("/reservations/update/1", json=payload)
        
        assert response.status_code == 200
        assert response.json()["status"] == "paid"
        mock_update.assert_called_once_with(1, payload)

def test_delete_reservation(client):
    with patch("app.controller.ReservationsController.reservations_service.delete_reservation") as mock_delete:
        mock_delete.return_value = True
        
        response = client.post("/reservations/delete/1")
        
        assert response.status_code == 200
        assert response.json() is True
        mock_delete.assert_called_once_with(1)

def test_service_create_reservation_expired_offer():
    from app.service.ReservationsService import ReservationsService
    from app.entity.OffersEntity import OffersEntity
    from datetime import datetime, timedelta
    
    service = ReservationsService()
    
    # Oferta expirada (pickup_end_time en el pasado)
    expired_offer = OffersEntity(
        id=10,
        business_id=1,
        title="Bolsa Expirada",
        original_price=5000,
        discounted_price=1500,
        quantity_available=1,
        pickup_start_time=datetime.now() - timedelta(hours=2),
        pickup_end_time=datetime.now() - timedelta(hours=1),
        status="active"
    )
    
    reservation_req = ReservationsEntity(
        user_id="user-123",
        offer_id=10,
        quantity=1,
        total_price=0.0,
        status="pending"
    )
    
    with patch.object(service.offers_repository, "get_by_id", return_value=expired_offer):
        with pytest.raises(ValueError) as exc_info:
            service.create_reservation(reservation_req)
        assert "El horario de retiro para esta oferta ya ha expirado" in str(exc_info.value)

def test_service_create_reservation_active_offer():
    from app.service.ReservationsService import ReservationsService
    from app.entity.OffersEntity import OffersEntity
    from datetime import datetime, timedelta
    
    service = ReservationsService()
    
    # Oferta vigente (pickup_end_time en el futuro)
    active_offer = OffersEntity(
        id=10,
        business_id=1,
        title="Bolsa Vigente",
        original_price=5000,
        discounted_price=1500,
        quantity_available=1,
        pickup_start_time=datetime.now() - timedelta(hours=1),
        pickup_end_time=datetime.now() + timedelta(hours=1),
        status="active"
    )
    
    reservation_req = ReservationsEntity(
        user_id="user-123",
        offer_id=10,
        quantity=1,
        total_price=0.0,
        status="pending"
    )
    
    mock_res_db = ReservationsEntity(
        id=1,
        user_id="user-123",
        offer_id=10,
        quantity=1,
        total_price=1500.0,
        status="pending"
    )
    
    with patch.object(service.offers_repository, "get_by_id", return_value=active_offer), \
         patch.object(service.reservations_repository, "create", return_value=mock_res_db) as mock_create:
         
        res = service.create_reservation(reservation_req)
        assert res.id == 1
        assert res.total_price == 1500.0
        mock_create.assert_called_once()

def test_cancel_reservation_endpoint_success(client, mock_user_profile):
    mock_cancelled = ReservationsEntity(
        id=1,
        user_id=mock_user_profile.id,
        offer_id=10,
        quantity=2,
        total_price=6000.0,
        status="cancelled"
    )
    
    with patch("app.controller.ReservationsController.reservations_service.cancel_reservation") as mock_cancel:
        mock_cancel.return_value = mock_cancelled
        
        response = client.post("/reservations/cancel/1")
        
        assert response.status_code == 200
        assert response.json()["status"] == "cancelled"
        mock_cancel.assert_called_once_with(
            id_val=1,
            user_id=mock_user_profile.id,
            user_role=mock_user_profile.role
        )

def test_cancel_reservation_endpoint_error(client):
    with patch("app.controller.ReservationsController.reservations_service.cancel_reservation") as mock_cancel:
        mock_cancel.side_effect = ValueError("La reserva no existe.")
        
        response = client.post("/reservations/cancel/99")
        
        assert response.status_code == 400
        assert "La reserva no existe" in response.json()["detail"]

def test_service_cancel_reservation_success():
    from app.service.ReservationsService import ReservationsService
    service = ReservationsService()
    
    existing_reservation = ReservationsEntity(
        id=1,
        user_id="user-123",
        offer_id=10,
        quantity=2,
        total_price=6000.0,
        status="pending"
    )
    
    updated_reservation = ReservationsEntity(
        id=1,
        user_id="user-123",
        offer_id=10,
        quantity=2,
        total_price=6000.0,
        status="cancelled"
    )
    
    with patch.object(service, "get_reservation_by_id", return_value=existing_reservation), \
         patch.object(service, "update_reservation", return_value=updated_reservation) as mock_update:
         
        res = service.cancel_reservation(id_val=1, user_id="user-123", user_role="customer")
        assert res.status == "cancelled"
        mock_update.assert_called_once_with(1, {"status": "cancelled"})

def test_service_cancel_reservation_forbidden():
    from app.service.ReservationsService import ReservationsService
    service = ReservationsService()
    
    existing_reservation = ReservationsEntity(
        id=1,
        user_id="user-123",
        offer_id=10,
        quantity=2,
        total_price=6000.0,
        status="pending"
    )
    
    with patch.object(service, "get_reservation_by_id", return_value=existing_reservation):
        with pytest.raises(ValueError) as exc_info:
            # Intenta cancelar usuario 'user-456' con rol 'customer' (no es dueño ni admin)
            service.cancel_reservation(id_val=1, user_id="user-456", user_role="customer")
        assert "No tienes permiso para cancelar esta reserva" in str(exc_info.value)

def test_service_cancel_reservation_collected():
    from app.service.ReservationsService import ReservationsService
    service = ReservationsService()
    
    existing_reservation = ReservationsEntity(
        id=1,
        user_id="user-123",
        offer_id=10,
        quantity=2,
        total_price=6000.0,
        status="collected"
    )
    
    with patch.object(service, "get_reservation_by_id", return_value=existing_reservation):
        with pytest.raises(ValueError) as exc_info:
            service.cancel_reservation(id_val=1, user_id="user-123", user_role="customer")
        assert "No se puede cancelar una reserva que ya ha sido retirada" in str(exc_info.value)

def test_pay_reservation_endpoint_success(client, mock_user_profile):
    mock_paid = ReservationsEntity(
        id=1,
        user_id=mock_user_profile.id,
        offer_id=10,
        quantity=2,
        total_price=6000.0,
        status="paid"
    )
    
    with patch("app.controller.ReservationsController.reservations_service.pay_reservation") as mock_pay:
        mock_pay.return_value = mock_paid
        
        response = client.post("/reservations/pay/1")
        
        assert response.status_code == 200
        assert response.json()["status"] == "paid"
        mock_pay.assert_called_once_with(
            id_val=1,
            user_id=mock_user_profile.id
        )

def test_pay_reservation_endpoint_error(client):
    with patch("app.controller.ReservationsController.reservations_service.pay_reservation") as mock_pay:
        mock_pay.side_effect = ValueError("La reserva ya ha sido pagada.")
        
        response = client.post("/reservations/pay/1")
        
        assert response.status_code == 400
        assert "La reserva ya ha sido pagada" in response.json()["detail"]

def test_service_pay_reservation_success():
    from app.service.ReservationsService import ReservationsService
    from datetime import datetime
    service = Background_service = ReservationsService()
    
    existing_reservation = ReservationsEntity(
        id=1,
        user_id="user-123",
        offer_id=10,
        quantity=2,
        total_price=6000.0,
        status="pending",
        created_at=datetime.now()
    )
    
    updated_reservation = ReservationsEntity(
        id=1,
        user_id="user-123",
        offer_id=10,
        quantity=2,
        total_price=6000.0,
        status="paid",
        created_at=datetime.now()
    )
    
    with patch.object(service, "get_reservation_by_id", return_value=existing_reservation), \
         patch.object(service, "update_reservation", return_value=updated_reservation) as mock_update:
         
        res = service.pay_reservation(id_val=1, user_id="user-123")
        assert res.status == "paid"
        mock_update.assert_called_once_with(1, {"status": "paid"})

def test_service_pay_reservation_forbidden():
    from app.service.ReservationsService import ReservationsService
    service = ReservationsService()
    
    existing_reservation = ReservationsEntity(
        id=1,
        user_id="user-123",
        offer_id=10,
        quantity=2,
        total_price=6000.0,
        status="pending"
    )
    
    with patch.object(service, "get_reservation_by_id", return_value=existing_reservation):
        with pytest.raises(ValueError) as exc_info:
            service.pay_reservation(id_val=1, user_id="user-456")
        assert "No tienes permiso para pagar esta reserva" in str(exc_info.value)

def test_service_pay_reservation_expired_timeout():
    from app.service.ReservationsService import ReservationsService
    from datetime import datetime, timedelta
    service = ReservationsService()
    
    # Creada hace 20 minutos
    existing_reservation = ReservationsEntity(
        id=1,
        user_id="user-123",
        offer_id=10,
        quantity=2,
        total_price=6000.0,
        status="pending",
        created_at=datetime.now() - timedelta(minutes=20)
    )
    
    with patch.object(service, "get_reservation_by_id", return_value=existing_reservation), \
         patch.object(service, "update_reservation") as mock_update:
         
        with pytest.raises(ValueError) as exc_info:
            service.pay_reservation(id_val=1, user_id="user-123")
        
        assert "El tiempo límite de 15 minutos para pagar ha expirado" in str(exc_info.value)
        # Se debe haber cancelado automáticamente
        mock_update.assert_called_once_with(1, {"status": "cancelled"})
