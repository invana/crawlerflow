import uuid


def generate_random_id():
    return str(uuid.uuid4().hex)
