import ulid

def is_ulid(value: str) -> bool:
    try:
        ulid.from_str(value)
        return True
    except (ValueError, TypeError):
        return False