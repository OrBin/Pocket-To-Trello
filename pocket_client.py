from logging import Logger
from typing import Dict, Any
from pocket import Pocket

from config import AUTH_DATA_KEY


def load_pocket_client(conf_data: Dict[str, Any], logger: Logger) -> Pocket:
    pocket_client = Pocket(
        conf_data[AUTH_DATA_KEY]['pocket_consumer_key'],
        conf_data[AUTH_DATA_KEY]['pocket_user_credentials']['access_token'],
    )
    logger.info('Logged in to Pocket')
    return pocket_client
