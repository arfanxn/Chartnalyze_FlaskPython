from flask import Flask
from app.config import Config
import click
import time
import requests
import threading
import time

success_count = 0
failure_count = 0
lock = threading.Lock()

def register_test_commands(app: Flask):

    @app.cli.command('test-ddos-should-error-with-429')
    @click.argument('url', type=str, default=f"{Config.API_URL}/api/users/register")
    @click.option('--request-count', '-r', type=int, default=100, help='Total number of requests to send.')
    @click.option('--thread-count', '-t', type=int, default=10, help='Number of concurrent threads.')
    def test_ddos_should_error_with_429(url, request_count, thread_count):
        with app.app_context():
            global success_count, failure_count
            success_count = 0
            failure_count = 0

            print('Testing DDOS...')
            print(f"URL: {url}")
            print(f"Request Count: {request_count}")
            print(f"Thread Count: {thread_count}")

            start_time = time.time()
            
            threads = []

            def send_request():
                global success_count, failure_count
                while sum([success_count, failure_count]) < request_count:
                    try:
                        response = requests.get(url, timeout=5)
                        if response.status_code != 429:
                            with lock:
                                if sum([success_count, failure_count]) < request_count:
                                    success_count += 1
                                    print('.', end='', flush=True) 
                        else:
                            with lock:
                                if sum([success_count, failure_count]) < request_count:
                                    failure_count += 1
                                    print('E', end='', flush=True) 
                    except requests.exceptions.RequestException:
                        with lock:
                            if sum([success_count, failure_count]) < request_count:
                                failure_count += 1
                                print('F', end='', flush=True) 

            for i in range(thread_count):
                thread = threading.Thread(target=send_request)
                thread.daemon = True
                threads.append(thread)
                thread.start()

            for thread in threads:
                while thread.is_alive() and sum([success_count, failure_count]) < request_count:
                    time.sleep(0.1)

            end_time = time.time()
            duration = end_time - start_time

            print('\nDDOS completed')
            print(f"Duration: {duration:.2f} seconds")
            print(f"Successful request count: {success_count}")
            print(f"Failed request count: {failure_count}")
            if duration > 0:
                rps = success_count / duration
                print(f"Requests Per Second (RPS): {rps:.2f}")
