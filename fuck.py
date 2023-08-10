from models import *

self = Item()

representation = {}
attrs = dir(self)
for attr in attrs:
    if attr.startswith("__") or attr == "dict":
        continue
    representation[attr] = eval(f"self.{attr}")


for key, value in representation.items():
    print(key)
    try:
        print(value)
    except RecursionError:
        print("recursion")
        break
    print()
