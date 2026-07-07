import pytest
from unittest.mock import patch
from app.entity.UserEntity import UserEntity
from app.entity.ReservationsEntity import ReservationsEntity
from app.controller.AuthController import get_current_user_profile

def test_register_success(client):
    register_payload = {
        "email": "newuser@example.com",
        "password": "securepassword",
        "name": "New User",
        "phone": "+56999999999",
        "role": "customer"
    }
    
    mock_registered_user = UserEntity(
        id="new-uuid-123",
        email="newuser@example.com",
        name="New User",
        phone="+56999999999",
        role="customer"
    )
    
    with patch("app.controller.AuthController.user_service.register") as mock_register:
        mock_register.return_value = mock_registered_user
        
        response = client.post("/auth/register", json=register_payload)
        
        assert response.status_code == 200
        assert response.json()["email"] == "newuser@example.com"
        assert response.json()["id"] == "new-uuid-123"
        mock_register.assert_called_once_with(
            email="newuser@example.com",
            password="securepassword",
            name="New User",
            phone="+56999999999",
            role="customer",
            business_id=None
        )

def test_register_invalid_role(client):
    register_payload = {
        "email": "newuser@example.com",
        "password": "securepassword",
        "role": "super-admin"
    }
    
    response = client.post("/auth/register", json=register_payload)
    assert response.status_code == 400
    assert "Invalid role" in response.json()["detail"]

def test_login_success(client):
    login_payload = {
        "email": "test@example.com",
        "password": "password123"
    }
    
    mock_login_response = {
        "access_token": "mock-access-token",
        "refresh_token": "mock-refresh-token",
        "expires_in": 3600,
        "token_type": "bearer",
        "user": {
            "id": "mock-user-uuid-123",
            "email": "test@example.com",
            "role": "customer"
        }
    }
    
    with patch("app.controller.AuthController.user_service.login") as mock_login:
        mock_login.return_value = mock_login_response
        
        response = client.post("/auth/login", json=login_payload)
        
        assert response.status_code == 200
        assert response.json()["access_token"] == "mock-access-token"
        assert response.json()["user"]["email"] == "test@example.com"
        mock_login.assert_called_once_with(email="test@example.com", password="password123")

def test_login_failure(client):
    login_payload = {
        "email": "test@example.com",
        "password": "wrongpassword"
    }
    
    with patch("app.controller.AuthController.user_service.login") as mock_login:
        mock_login.side_effect = Exception("Credenciales inválidas.")
        
        response = client.post("/auth/login", json=login_payload)
        
        assert response.status_code == 400
        assert response.json()["detail"] == "Credenciales inválidas."

def test_get_profile_success(client, mock_user_profile):
    response = client.get("/auth/profile")
    assert response.status_code == 200
    assert response.json()["email"] == mock_user_profile.email
    assert response.json()["id"] == mock_user_profile.id

def test_update_profile_success(client, mock_user_profile):
    update_payload = {
        "name": "Updated Name",
        "phone": "+56988888888"
    }
    
    mock_updated_user = UserEntity(
        id=mock_user_profile.id,
        email=mock_user_profile.email,
        name="Updated Name",
        phone="+56988888888",
        role=mock_user_profile.role
    )
    
    with patch("app.controller.AuthController.user_service.update_user") as mock_update_user:
        mock_update_user.return_value = mock_updated_user
        
        response = client.patch("/auth/profile", json=update_payload)
        
        assert response.status_code == 200
        assert response.json()["name"] == "Updated Name"
        assert response.json()["phone"] == "+56988888888"
        mock_update_user.assert_called_once_with(mock_user_profile.id, update_payload)

def test_update_profile_no_data(client):
    response = client.patch("/auth/profile", json={})
    assert response.status_code == 400
    assert "No se enviaron campos válidos" in response.json()["detail"]

def test_get_user_reservations(client, mock_supabase_user):
    mock_reservations = [
        ReservationsEntity(id=1, offer_id=10, user_id=mock_supabase_user.id, quantity=2, total_price=5000.0, status="pending")
    ]
    
    with patch("app.controller.AuthController.user_service.get_user_reservations") as mock_get_reservations:
        mock_get_reservations.return_value = mock_reservations
        
        response = client.get("/auth/reservations")
        
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["id"] == 1
        mock_get_reservations.assert_called_once_with(mock_supabase_user.id)

def test_link_worker_as_admin_success(client, mock_admin_profile):
    from app.main import app
    app.dependency_overrides[get_current_user_profile] = lambda: mock_admin_profile
    
    payload = {"user_id": "target-uuid-1", "business_id": 5}
    mock_linked_user = UserEntity(id="target-uuid-1", email="target@worker.cl", role="worker", business_id=5)
    
    with patch("app.controller.AuthController.user_service.link_worker") as mock_link:
        mock_link.return_value = mock_linked_user
        
        response = client.post("/auth/link-worker", json=payload)
        
        assert response.status_code == 200
        assert response.json()["business_id"] == 5
        mock_link.assert_called_once_with(
            target_user_id="target-uuid-1",
            target_business_id=5,
            caller_user_id=mock_admin_profile.id,
            caller_role=mock_admin_profile.role,
            caller_business_id=mock_admin_profile.business_id
        )

def test_link_worker_as_worker_same_business_success(client, mock_worker_profile):
    from app.main import app
    app.dependency_overrides[get_current_user_profile] = lambda: mock_worker_profile
    
    # El worker pertenece al business_id=1, y vincula a un target al business_id=1
    payload = {"user_id": "target-uuid-2", "business_id": 1}
    mock_linked_user = UserEntity(id="target-uuid-2", email="target2@worker.cl", role="worker", business_id=1)
    
    with patch("app.controller.AuthController.user_service.link_worker") as mock_link:
        mock_link.return_value = mock_linked_user
        
        response = client.post("/auth/link-worker", json=payload)
        
        assert response.status_code == 200
        assert response.json()["business_id"] == 1
        mock_link.assert_called_once()

def test_link_worker_as_worker_different_business_forbidden(client, mock_worker_profile):
    from app.main import app
    app.dependency_overrides[get_current_user_profile] = lambda: mock_worker_profile
    
    # El worker pertenece al business_id=1, e intenta vincular a un target al business_id=2 (ajeno)
    payload = {"user_id": "target-uuid-2", "business_id": 2}
    
    with patch("app.controller.AuthController.user_service.link_worker") as mock_link:
        mock_link.side_effect = ValueError("No tienes permiso para vincular trabajadores a un local comercial ajeno.")
        
        response = client.post("/auth/link-worker", json=payload)
        
        assert response.status_code == 403
        assert "No tienes permiso" in response.json()["detail"]

def test_link_worker_target_not_worker_error(client, mock_admin_profile):
    from app.main import app
    app.dependency_overrides[get_current_user_profile] = lambda: mock_admin_profile
    
    payload = {"user_id": "customer-uuid-3", "business_id": 1}
    
    with patch("app.controller.AuthController.user_service.link_worker") as mock_link:
        mock_link.side_effect = ValueError("El usuario destino debe tener el rol de 'worker'.")
        
        response = client.post("/auth/link-worker", json=payload)
        
        assert response.status_code == 400
        assert "El usuario destino debe tener" in response.json()["detail"]

def test_service_link_worker_success():
    from app.service.UserService import UserService
    service = UserService()
    
    target_user = UserEntity(id="target-uuid", email="target@example.com", role="worker", business_id=None)
    updated_user = UserEntity(id="target-uuid", email="target@example.com", role="worker", business_id=5)
    
    # Caso: admin vincula worker a business 5
    with patch.object(service, "get_user_byid", return_value=target_user), \
         patch.object(service, "update_user", return_value=updated_user) as mock_update:
         
        res = service.link_worker(
            target_user_id="target-uuid",
            target_business_id=5,
            caller_user_id="admin-uuid",
            caller_role="admin",
            caller_business_id=None
        )
        assert res.business_id == 5
        mock_update.assert_called_once_with("target-uuid", {"business_id": 5})

def test_service_link_worker_invalid_role():
    from app.service.UserService import UserService
    service = UserService()
    
    # Caso: target es un 'customer' en lugar de 'worker'
    target_user = UserEntity(id="target-uuid", email="target@example.com", role="customer", business_id=None)
    
    with patch.object(service, "get_user_byid", return_value=target_user):
        with pytest.raises(ValueError) as exc_info:
            service.link_worker(
                target_user_id="target-uuid",
                target_business_id=5,
                caller_user_id="admin-uuid",
                caller_role="admin",
                caller_business_id=None
            )
        assert "El usuario destino debe tener el rol de 'worker'" in str(exc_info.value)

