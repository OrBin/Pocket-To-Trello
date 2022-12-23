import logging
from os.path import dirname, abspath
from pathlib import Path
from datetime import datetime

from config import load_config
from convert import convert_single_item
from pocket_client import load_pocket_client
from state import select_state_manager
from trello_client import load_trello_client


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

# Reading configuration and authentication data
conf_data = load_config()
pocket_client = load_pocket_client(conf_data, logger)
trello_client = load_trello_client(conf_data, logger)
trello_list = trello_client.get_list(conf_data['trello_list_id'])

now_timestamp = int(datetime.now().timestamp())
state_manager = select_state_manager(logger)
logger.info('Selected state manager: %s', state_manager.__class__.__name__)
since_timestamp = int(state_manager.read(default=str(now_timestamp)))

new_pocket_items, _ = pocket_client.get(since=since_timestamp)
logger.info('Fetched new Pocket items')

if len(new_pocket_items['list']) == 0:
    logger.info('No new items')
else:
    for pocket_item_id, pocket_item_data in new_pocket_items['list'].items():
        convert_single_item(pocket_item_id, pocket_item_data, trello_list, logger, since_timestamp)

state_manager.write(str(now_timestamp))
