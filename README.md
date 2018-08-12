# Pocket-To-Trello
A utility to create cards in a reading board in Trello out of new items saved to Pocket

## Usage

### Installing requirements
```
pip install -r requirements.txt
```

### Get Pocket consumer key
[Create a new Pocket app](https://getpocket.com/developer/apps/new) with "Retrieve" permission and save the generated consumer key for later use.

### Get Trello API key
Visit [here](https://trello.com/app-key) to get your Trello API key and save it for later use.

### Creating a configuration file
A configuration file `config.json` should be placed in the same directory as the code files.

Here is an example of how the initial configuration file should look:
```
{
  "authentication": {
    "pocket_consumer_key": "YOUR-POCKET-CONSUMER-KEY",
    "trello_api_key": "YOUR-TRELLO-API-KEY",
  },
  "pocket_last_checked": 0,
  "trello_list_id": "YOUR-TRELLO-LIST-ID"
}
```

### Authorizing with Pocket and Trello (Should be done only once)
Authorize with Pocket:
```
python authorize_pocket.py
```
Authorize with Trello:
```
python authorize_trello.py
```

### Run
```
python main.py
```

### (Optional) Add to cron
You can create a cron job with the following configuration to run the app every 10 minutes:
```
*/10 * * * * python /path/to/repository/Pocket-To-Trello/main.py
```
