from app.repository.MlHistoricalDataRepository import MlHistoricalDataRepository

class MlHistoricalDataService:
    def __init__(self):
        self.ml_historical_data_repository = MlHistoricalDataRepository()
