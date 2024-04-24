# Placeholder data structure to store key-value and hash data
data_store = {}
hash_store = {}

def PING(resp):
    resp.write_status("PONG")

def SET(resp, key, value):
    data_store[key] = value
    resp.write_status("OK")

def GET(resp, key):
    value = data_store.get(key, "nil")
    resp.write_bulk(value)

def HSET(resp, key, field, value):
    if key not in hash_store:
        hash_store[key] = {}
    hash_store[key][field] = value
    resp.write_status("OK")

def HGET(resp, key, field):
    value = hash_store.get(key, {}).get(field, "nil")
    resp.write_bulk(value)

def HGETALL(resp, key):
    values = []
    hash_data = hash_store.get(key, {})
    for field, value in hash_data.items():
        values.extend([field, value])
    resp.write_array(values)
