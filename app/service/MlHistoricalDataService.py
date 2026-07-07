"""ML Historical Data Service.

This module defines the MlHistoricalDataService class which manages machine learning data retrieval operations.
"""

from app.repository.MlHistoricalDataRepository import MlHistoricalDataRepository

class MlHistoricalDataService:
    """Service class encapsulating logic for machine learning historical data."""

    def __init__(self):
        """Initializes the service by setting up the MlHistoricalDataRepository."""
        self.ml_historical_data_repository = MlHistoricalDataRepository()
