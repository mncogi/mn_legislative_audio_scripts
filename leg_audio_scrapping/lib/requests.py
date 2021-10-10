import logging
import requests
from requests_file import FileAdapter

requests_session = requests.session()
requests_session.mount('file://', FileAdapter())


def web_get(uri):
    """Get file at the provided URI. Supports fetching files with `file://` schema."""
    logging.info(f'Fetching {uri}')
    return requests_session.get(uri)
