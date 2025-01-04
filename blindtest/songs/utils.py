from django.utils.crypto import get_random_string


def create_token():
    token = get_random_string(length=5)
    return f'tok_{token}'
