import json
from pocket import Pocket


CONFIG_FILE_NAME = 'config.json'
AUTH_DATA_KEY = 'authentication'

with open(CONFIG_FILE_NAME, 'r') as conf_file:
    conf_data = json.load(conf_file)
auth_data = conf_data[AUTH_DATA_KEY]

pocket_consumer_key = auth_data['pocket_consumer_key']
pocket_redirect_uri = 'https://getpocket.com'

request_token = Pocket.get_request_token(consumer_key=pocket_consumer_key, redirect_uri=pocket_redirect_uri)
auth_url = Pocket.get_auth_url(code=request_token, redirect_uri=pocket_redirect_uri)

print('Please visit the following URL and press \'Authorize\' (if not automatically redirected) to continue:')
print(auth_url)
input("Press Enter when done to continue...")

user_credentials = Pocket.get_credentials(consumer_key=pocket_consumer_key, code=request_token)

auth_data['pocket_user_credentials'] = user_credentials
with open(CONFIG_FILE_NAME, 'w') as conf_file:
    json.dump(conf_data, conf_file, indent=2)
