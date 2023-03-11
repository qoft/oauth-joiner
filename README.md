# Oauth Joiner
 
Joins all of your tokens into a guild ID you provide without captchas.

## Installation

```bash
git clone qoft/oauth-joiner
cd oauth-joiner
pip install -r requirements.txt
copy config.py.example config.py
python main.py
```

## Requirements

Python 3.7+

A brain

Discord tokens

## Usage

Go to [Discord Developer Page](https://discord.com/developers/applications) and make a new application


### Getting the Client ID and Client Secret
Press on the `OAuth2` tab

Add `http://localhost:8080/oauth2` as a redirect

Copy the `Client ID` and `Client Secret` into `config.py`


### Getting the bot token

Press on the `Bot` tab

Click the blue `Add Bot` button and create a bot.

Copy the token and paste it into `config.py`

### Running the bot

Copy all of your tokens into `data/tokens.txt`

Input your `Guild ID` of your server into `config.py`

Make sure the Discord Bot is in your server

Run `main.py`



# Disclaimer
I am not responsible nor liable for anything that you do with this. 

This is for educational purposes only.
