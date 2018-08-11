import sys
import json
import requests
from pocket import Pocket
from datetime import datetime
from bs4 import BeautifulSoup


CONFIG_FILE_NAME = 'config.json'
AUTH_DATA_KEY = 'authentication'

# Reading configuration and authentication data
with open(CONFIG_FILE_NAME, 'r') as conf_file:
    conf_data = json.load(conf_file)
auth_data = conf_data[AUTH_DATA_KEY]

# Logging in to Pocket
pocket_consumer_key = conf_data[AUTH_DATA_KEY]['pocket_consumer_key']
pocket_instance = Pocket(conf_data[AUTH_DATA_KEY]['pocket_consumer_key'],
                         conf_data[AUTH_DATA_KEY]['pocket_user_credentials']['access_token'])

# Logging in to Trello
# TODO

now_timestamp = int(datetime.now().timestamp())
since_timestamp = conf_data['pocket_last_checked'] if 'pocket_last_checked' in conf_data else now_timestamp

response_data, _ = pocket_instance.get(since=since_timestamp)

if len(response_data['list']) == 0:
    print('No new items.')
    sys.exit(0)

for item_id, item_data in response_data['list'].items():
    with requests.get(item_data['given_url']) as page_response:
        parsed_page = BeautifulSoup(page_response.text, 'html.parser')
    page_title = parsed_page.title.text

    print(page_title)
    print(item_data['given_url'])
    print(item_data['excerpt'])

    # TODO save item to Trello


conf_data['pocket_last_checked'] = now_timestamp
with open(CONFIG_FILE_NAME, 'w') as conf_file:
    json.dump(conf_data, conf_file, indent=2)