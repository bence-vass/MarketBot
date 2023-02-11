SUPPORTED_API_SERVICES = [
    'polygon.io',
    'other'
]


def connect_client(api_service, api_key):
    if api_service not in SUPPORTED_API_SERVICES:
        raise Exception('Unsupported API Service')

    match api_service:
        case 'polygon.io':
            print("Connect to Polygon.io")
            from .polygon_io import create_client
            return create_client(api_key=api_key)

        case 'other':
            print("Connect to other API service")
