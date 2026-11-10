def rehydrate(response: str, mapping: dict) -> str:
    for placeholder in sorted(mapping, key=len, reverse=True):
        response = response.replace(placeholder, mapping[placeholder])
    return response
