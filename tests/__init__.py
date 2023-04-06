"""

By Allen Tao
Created at 2023/02/10 15:36
"""
from dotenv import load_dotenv

load_dotenv(verbose=True)
_data = {}


def create_test_client():
    from main import app

    return app.test_client()


BASE_URL = 'http://localhost:5000'
client = create_test_client()
