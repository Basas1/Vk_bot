# VK BOT VLADIMIR
Chat-bot for social networking service vk.com that can:  
* Chat with user
* Generate and send a playlist of specified artist's most popular songs
* Generate and send a playlist of similar to specified artist music


## Getting Started
### Requirements
* Python 3
* You will need to install the following libraries:  
    1. vk_api: `pip install vk_api`
    2. requests: `pip install requests`
    3. selenium: `pip install selenium`
* Account on vk.com
* API Keys for:  
    1. cleverbot.com
    2. last.fm  

### Installation
On Windows:  
First you will need to rename `settings_example.py` file to `settings.py` and fill it in with your personal 
account data and API keys.  
Then open command line in the directory `~/Vk_bot` and run the next command in it: `pip install .`

## How to use
Once you installed and launched bot.py you can send personal messages to vk-user attached to bot-login stated 
in settings.py. Also, you can add it to chat rooms. Bot will read all inbox messages and reply to them if it 
stars with the next prefixes:  
* **!help** - wil send reply message with the list of supported commands;  
* **!p artist name** - Generate and send a playlist of artist's most popular songs;  
* **!s artist name** - Generate and send a playlist of similar to artist music;  
* **!вов message** or **!c message** is used to chat with bot in chat rooms. Bot will generate the answer to message
and send it to chat with prefix consisting of "Name of the user that send message, bot's answer".  

In personal messages last command is used by default and bot does not include name prefix to reply.


## Authors
* **Nikolay** - [Basas1](https://github.com/Basas1)
* **Mikhail** - [direday](https://github.com/direday)

