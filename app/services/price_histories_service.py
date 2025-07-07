import pandas as pd

from app.services import Service
from app.repositories import PriceHistoriesRepository
from flask import g

ph_repository = PriceHistoriesRepository()

class PriceHistoriesService(Service):

    def __init__(self):
        super().__init__()
    
    def all_by_symbol (self, symbol: str) -> tuple[list[object]]:
        price_histories, = ph_repository.all_by_symbol(symbol=symbol)
        return (price_histories, )
    
    def all_distinct_symbols(self) -> tuple[list[object]]:
        symbols, = ph_repository.all_distinct_symbols()
        return (symbols, )