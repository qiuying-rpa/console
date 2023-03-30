"""

By Ziqiu Li
Created at 2023/3/29 23:02
"""
import time
from utils.repository import use_redis


def test_redis():
    redis_conn = use_redis()
    redis_conn.set(name='token', value='123')
    assert redis_conn.get(name='token') == '123'
    redis_conn.set(name='token1', value='1234', ex=5)
    time.sleep(6)
    assert redis_conn.get(name='token1') is None
    redis_conn.delete(*['token'])
    assert redis_conn.get(name='token') is None
