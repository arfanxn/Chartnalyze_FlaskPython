# scraper.py
from flask import Flask
from datetime import datetime, timedelta
from app.extensions import mongo
from app import extensions
import concurrent.futures

def register_scraper_commands(app: Flask):

    @app.cli.command('scrap-price-histories-then-insert')
    def scrap_price_history_then_insert():
        with app.app_context():
            print('Scraping price histories...')
            cg = extensions.coingecko 

            coins = cg.get_coins_markets(vs_currency='usd', per_page=100, page=1)
            coin_map = {c['symbol'].upper(): c['id'] for c in coins}

            collection = mongo.db.price_histories

            now = datetime.now()
            from_timestamp = int((now - timedelta(days=30)).timestamp())
            to_timestamp = int(now.timestamp())

            def fetch_and_insert_prices(symbol, gecko_id):
                """
                Fetches price history for a single coin, finds new data points,
                and bulk-inserts them into the database.
                """
                try:
                    # 1. API Call: Fetch 30 days of price data for the coin
                    chart_data = cg.get_coin_market_chart_range_by_id(
                        id=gecko_id,
                        vs_currency='usd',
                        from_timestamp=from_timestamp,
                        to_timestamp=to_timestamp
                    )
                    prices = chart_data.get('prices', [])
                    if not prices:
                        print(f"No price data returned for \"{symbol}\".")
                        return 0

                    # 2. Prepare documents and get their timestamps
                    potential_entries = []
                    timestamps_to_check = []
                    for price_point in prices:
                        # Convert millisecond timestamp to datetime object
                        ts = datetime.fromtimestamp(price_point[0] / 1000)
                        potential_entries.append({
                            'symbol': symbol,
                            'scraped_at': ts,
                            'price_usd': price_point[1]
                        })
                        timestamps_to_check.append(ts)

                    # 3. Bulk Database Read: Find all timestamps that ALREADY exist in the DB for this coin
                    # This is one efficient query instead of one query per data point.
                    query = {'symbol': symbol, 'scraped_at': {'$in': timestamps_to_check}}
                    projection = {'_id': 0, 'scraped_at': 1}
                    existing_timestamps = {doc['scraped_at'] for doc in collection.find(query, projection)}

                    # 4. Filter in Memory: Determine which entries are new by checking against the existing timestamps
                    entries_to_insert = [
                        entry for entry in potential_entries if entry['scraped_at'] not in existing_timestamps
                    ]
                    
                    # 5. Bulk Database Write: Insert all new documents in a single operation
                    if entries_to_insert:
                        collection.insert_many(entries_to_insert)
                        print(f"Inserted {len(entries_to_insert)} new price history entries for \"{symbol}\".")
                        return len(entries_to_insert)
                    
                    print(f"Price history for \"{symbol}\" is already up to date.")
                    return 0

                except Exception as e:
                    raise e

            # --- Main execution with concurrency ---
            total_inserted = 0
            # Use a ThreadPoolExecutor to run API requests concurrently (max_workers can be tuned)
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                # Create a future for each coin processing task
                future_to_coin = {executor.submit(fetch_and_insert_prices, symbol, gecko_id): symbol for symbol, gecko_id in coin_map.items()}
                
                # Process results as they are completed
                for future in concurrent.futures.as_completed(future_to_coin):
                    try:
                        # Get the number of inserted documents from the function's return value
                        inserted_count = future.result()
                        total_inserted += inserted_count
                    except Exception as e:
                        coin_symbol = future_to_coin[future]
                        print(f"Task for \"{coin_symbol}\" generated an exception: {e}")

            print(f"\nScraping complete. {total_inserted} total new price history entries inserted.")