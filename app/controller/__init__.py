"""Controllers package initialization.

This module aggregates and registers all controller routers into a single APIRouter instance.
"""

from fastapi import APIRouter
from .AuthController import router as auth_router
from .BusinessesController import router as business_router
from .OffersController import router as offers_router
from .FoodBanksController import router as food_banks_router
from .DonationsController import router as donations_router
from .UserFavoritesController import router as user_favorites_router
from .ReservationsController import router as reservations_router
from .ReviewsController import router as reviews_router

api_router = APIRouter()

# Registro manual de todos los sub-routers
api_router.include_router(auth_router)
api_router.include_router(business_router)
api_router.include_router(offers_router)
api_router.include_router(food_banks_router)
api_router.include_router(donations_router)
api_router.include_router(user_favorites_router)
api_router.include_router(reservations_router)
api_router.include_router(reviews_router)
