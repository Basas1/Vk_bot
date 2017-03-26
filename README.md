# VK BOT VLADIMIR
Chat-bot for social networking service vk.com that can:  
* Chat with user
* Generate and send a playlist of artist's of your choice most popular songs
* Generate and send a playlist of similar to artist of your choice music


## Getting Started
### Requirements
* Python 3
* PhantomJS  
You can download it from official web-site:  
`http://phantomjs.org/`
* Account on vk.com
* API Keys for:  
    - cleverbot.com
    - last.fm  

### Installation
On Windows:  
First you will need to rename `settings_example.py` file to `settings.py` and fill it in with your personal 
account data and API keys. Specify your path to `phantomjs.exe` and save changes.  
Then open command line in the directory `~/Vk_bot` and run the following command in it: 
```bash
pip install .
```
This script will also download and install the following libraries if they haven't been installed yet:
- vk_api
- requests
- selenium

## How to use
Once you installed and launched `bot.py` you can send personal messages to vk-user attached to bot-login stated 
in `settings.py`. Also, you can add bot to chat rooms. He will read all inbox messages and reply to them if it 
starts with one of the following prefixes:  
* **!help** - will send reply message with the list of supported commands;  
* **!p artist name** - Generate and send a playlist of artist's most popular songs;  
* **!s artist name** - Generate and send a playlist of similar to artist music;  
* **!c message** or **!вов message** is used to chat with bot in chat rooms. Bot will generate the answer to message
and send it to chat with prefix consisting of "Name of the user that send message, bot's answer".  

In personal messages last command is used by default and bot does not include name prefix to reply.


## Authors
* **Nikolay** - [Basas1](https://github.com/Basas1)
* **Mikhail** - [direday](https://github.com/direday)

