import redis
import time
import json

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)