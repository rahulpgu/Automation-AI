import truststore
truststore.inject_into_ssl()

import httpx

try:
    r = httpx.get("https://models.inference.ai.azure.com")
    print(r.status_code)
except Exception as e:
    import traceback
    traceback.print_exc()