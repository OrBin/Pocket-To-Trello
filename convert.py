from logging import Logger
from typing import Any

import requests
from bs4 import BeautifulSoup
from trello import List as TrelloList


def convert_single_item(
        pocket_item_id: str,
        pocket_item_data: dict[str, Any],
        trello_list: TrelloList,
        logger: Logger,
        since_timestamp: int,
):
    # status - 0, 1, 2 - 1 if the item is archived - 2 if the item should be deleted
    if not pocket_item_data['status'] == '0':
        return

    # The 'since' parameter on Pocket.get relates to update time only, but we want to filter by add time
    item_add_timestamp = int(pocket_item_data['time_added'])
    if item_add_timestamp < since_timestamp:
        return

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
