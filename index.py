from custom_module import get_all_krw as getkrw
import redis 
from ast import literal_eval

getkrw.get_all_krw("localhost", 6379, 0)
r=redis.Redis(host="localhost", port=6379, db=0)
data=literal_eval("{"+r.get("XYM").decode("utf-8")+"}")
print(data["1685455938213"]["opening_price"])


