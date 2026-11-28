# Shared helper, kept tiny: stdlib only (the sandbox denies reading *.pem, which breaks certifi/httpx).
import json, urllib.request

def call(url, method="GET"):
    with urllib.request.urlopen(urllib.request.Request(url, method=method, data=b"" if method == "POST" else None)) as r:
        return r.status, json.loads(r.read())
