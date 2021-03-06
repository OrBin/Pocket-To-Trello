import sys
import json
import requests
import logging
import os
from os.path import join, dirname, abspath
from logging.handlers import RotatingFileHandler
from pocket import Pocket
from datetime import datetime
from bs4 import BeautifulSoup
from trello import TrelloClient


CONFIG_FILE_NAME = join(dirname(abspath(__file__)), 'config.json')
LOGS_DIR_PATH = join(dirname(abspath(__file__)), 'logs')
LOG_FILE_NAME = join(LOGS_DIR_PATH, 'pocket_to_trello.log')
AUTH_DATA_KEY = 'authentication'


# Enable logging
os.makedirs(LOGS_DIR_PATH, exist_ok=True)
file_handler = RotatingFileHandler(LOG_FILE_NAME, maxBytes=(1048576 * 5), backupCount=7)
console_handler = logging.StreamHandler()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    handlers=[file_handler, console_handler])
logger = logging.getLogger(__name__)

# Reading configuration and authentication data
with open(CONFIG_FILE_NAME, 'r') as conf_file:
    conf_data = json.load(conf_file)
auth_data = conf_data[AUTH_DATA_KEY]

# Logging in to Pocket
pocket_consumer_key = conf_data[AUTH_DATA_KEY]['pocket_consumer_key']
pocket_client = Pocket(conf_data[AUTH_DATA_KEY]['pocket_consumer_key'],
                       conf_data[AUTH_DATA_KEY]['pocket_user_credentials']['access_token'])
logger.info('Logged in to Pocket')

# Logging in to Trello
trello_client = TrelloClient(
    api_key=conf_data[AUTH_DATA_KEY]['trello_api_key'],
    token=conf_data[AUTH_DATA_KEY]['trello_token']
)
trello_list = trello_client.get_list(conf_data['trello_list_id'])
logger.info('Logged in to Trello')

now_timestamp = int(datetime.now().timestamp())
since_timestamp = conf_data['pocket_last_checked'] if 'pocket_last_checked' in conf_data else now_timestamp

new_pocket_items, _ = pocket_client.get(since=since_timestamp)
logger.info('Fetched new Pocket items')

if len(new_pocket_items['list']) == 0:
    logger.info('No new items.')
else:
    for pocket_item_id, pocket_item_data in new_pocket_items['list'].items():

        # status - 0, 1, 2 - 1 if the item is archived - 2 if the item should be deleted
        if not pocket_item_data['status'] == '0':
            continue

        # The 'since' parameter on Pocket.get relates to update time only, but we want to filter by add time
        item_add_timestamp = int(pocket_item_data['time_added'])
        if item_add_timestamp < since_timestamp:
            continue

        page_url = pocket_item_data['given_url']
        logger.info(f'Found item {page_url}')

        # Getting page title
        if page_url.endswith('.pdf'):
            page_title = page_url.split('/')[-1].split('.')[0]
        else:
            try:
                with requests.get(page_url) as page_response:
                    parsed_page = BeautifulSoup(page_response.text, 'html.parser')
                page_title = parsed_page.title.text
            except:
                page_title = page_url

        card = trello_list.add_card(name=page_title,
                                    desc=pocket_item_data['excerpt'])
        logger.info(f'Created card \'{page_title}\')')
        card.attach(name='Original article', url=page_url)
        card.attach(name='Pocket (web)', url=f'https://app.getpocket.com/read/{pocket_item_id}')
        card.attach(name='Pocket (mobile)', url=f'https://getpocket.com/a/read/{pocket_item_id}')
        logger.info(f'Attached links to card')

conf_data['pocket_last_checked'] = now_timestamp
with open(CONFIG_FILE_NAME, 'w') as conf_file:
    json.dump(conf_data, conf_file, indent=2)