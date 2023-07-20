import requests

index = 1
while index < 2800:
    res = requests.get(
        "http://127.0.0.1:8000/api/engine/run?method_pool_id={}".format(str(index))
    )

    print(res.status_code)
    print(res.content)
    print(index)
    index = index + 1
