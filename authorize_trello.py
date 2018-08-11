import json


CONFIG_FILE_NAME = 'config.json'
AUTH_DATA_KEY = 'authentication'
APP_NAME = 'Pocket%20to%20Trello'

with open(CONFIG_FILE_NAME, 'r') as conf_file:
    conf_data = json.load(conf_file)
auth_data = conf_data[AUTH_DATA_KEY]

trello_api_key = auth_data['trello_api_key']
auth_url = f'https://trello.com/1/authorize?expiration=never&scope=read,write&response_type=token&name={APP_NAME}&key={trello_api_key}'

print('Please visit the following URL and press \'Allow\' (if not automatically redirected) to continue:')
print(auth_url)
token = input('Copy and paste here the token you received: ')

auth_data['trello_token'] = token
with open(CONFIG_FILE_NAME, 'w') as conf_file:
    json.dump(conf_data, conf_file, indent=2)
