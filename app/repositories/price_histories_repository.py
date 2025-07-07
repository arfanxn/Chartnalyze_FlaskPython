from app.repositories.repository import Repository
from app.extensions import mongo
from flask import request

class PriceHistoriesRepository(Repository):

    def __init__(self):
        super().__init__()
    
    def all_by_symbol(self, symbol: str) -> tuple[list[object]]:
        filter = request.args.get('filter', None)

        find = {}
        find['symbol'] = symbol.upper()

        if filter is not None:
            regex_pattern = f".*{filter}.*"
            find['symbol'] = {"$regex": regex_pattern, "$options": "i"}

        cursor = mongo.db.price_histories.find(find)\
            .sort([('created_at', -1)]).limit(10)
        price_histories = list(cursor)
        return (price_histories, )
    
    def all_distinct_symbols(self) -> tuple[list[object]]:
        symbols = mongo.db.price_histories.distinct('symbol')
        symbols = sorted(symbols)
        return (symbols, )
