from logging import Logger
from typing import Dict, Any
from trello.trelloclient import TrelloClient

from config import AUTH_DATA_KEY


def load_trello_client(conf_data: Dict[str, Any], logger: Logger) -> TrelloClient:
    trello_client = TrelloClient(
        api_key=conf_data[AUTH_DATA_KEY]['trello_api_key'],
        token=conf_data[AUTH_DATA_KEY]['trello_token']
    )
    logger.info('Logged in to Trello')
    return trello_client
