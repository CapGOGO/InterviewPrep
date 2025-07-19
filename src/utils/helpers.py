def format_output(data):
    return "\n".join(str(item) for item in data)

def handle_api_request(url, params=None):
    import requests
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()