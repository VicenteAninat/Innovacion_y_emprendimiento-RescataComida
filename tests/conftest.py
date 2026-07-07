import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.controller.AuthController import get_current_user, get_current_user_profile
from app.entity.UserEntity import UserEntity

@pytest.fixture
def mock_supabase_user():
    user = MagicMock()
    user.id = "mock-user-uuid-123"
    user.email = "test@example.com"
    return user

@pytest.fixture
def mock_user_profile():
    return UserEntity(
        id="mock-user-uuid-123",
        name="Test User",
        email="test@example.com",
        phone="+56912345678",
        role="customer",
        business_id=None
    )

@pytest.fixture
def mock_worker_profile():
    return UserEntity(
        id="mock-worker-uuid-456",
        name="Test Worker",
        email="worker@example.com",
        phone="+56912345679",
        role="worker",
        business_id=1
    )

@pytest.fixture
def mock_admin_profile():
    return UserEntity(
        id="mock-admin-uuid-789",
        name="Test Admin",
        email="admin@example.com",
        phone="+56912345680",
        role="admin",
        business_id=None
    )

@pytest.fixture
def client(mock_supabase_user, mock_user_profile):
    # Por defecto, inyectamos un usuario tipo customer
    app.dependency_overrides[get_current_user] = lambda: mock_supabase_user
    app.dependency_overrides[get_current_user_profile] = lambda: mock_user_profile
    
    with TestClient(app) as c:
        yield c
        
    app.dependency_overrides.clear()
