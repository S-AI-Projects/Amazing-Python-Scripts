"""
Songs By Artist configuration module.

Contract:
- client_id (str): Spotify application Client ID. Defined at L12.
- secret_key (str): Spotify application Secret Key. Defined at L13.
- get_config() -> dict[str, str]: Returns dictionary mapping config keys to their values without mutating state. Defined at L15.
- validate_config(client_id: str, secret_key: str) -> bool: Returns True if non-empty string credentials are provided. Defined at L20.
"""

client_id = ""
secret_key = ""


def get_config():
    """Return dictionary of configuration settings."""
    return {"client_id": client_id, "secret_key": secret_key}


def validate_config(cid: str = None, skey: str = None):
    """Validate Spotify API credentials contract."""
    target_cid = client_id if cid is None else cid
    target_skey = secret_key if skey is None else skey
    return bool(
        isinstance(target_cid, str)
        and isinstance(target_skey, str)
        and len(target_cid.strip()) > 0
        and len(target_skey.strip()) > 0
    )
