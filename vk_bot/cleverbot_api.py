import requests

from vk_bot.settings import cleverbot_api_key as api_key
from vk_bot.settings import cleverbot_cs


class CleverBot:
    def __init__(self, vk, item):
        self.vk = vk
        self.item = item
        self.cs = cleverbot_cs
        self.url = "http://www.cleverbot.com/getreply?key=" + api_key

    # Обмен сообщениями с клеверботом
    def exchange_messages(self, message):
        print('=>', message)
        send_url = self.url + "&input=" + message + "&cs=" + self.cs
        send = requests.get(send_url)
        answer = send.json()['output']
        self.send_message_from_bot(answer)

    # Отправка сообщения пользователю
    def send_message_from_bot(self, message):
        print('< ' + message)
        if 'chat_id' in self.item:
            response = self.vk.session.users.get(user_ids=int(self.item['user_id']))
            name = response[0]['first_name']
            self.vk.respond(self.item, {'message': name + ', ' + message})
        else:
            self.vk.respond(self.item, {'message': message})