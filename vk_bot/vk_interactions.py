import re
import time
import vk_api

from vk_bot.get_playlist import VkPlaylist
from vk_bot.cleverbot_api import CleverBot


class Vk:
    def __init__(self, login, password):
        try:
            self.api = vk_api.VkApi(login, password)
            self.api.auth()
            self.values = {
                'out': 0,
                'offset': 0,
                'count': 20,
                'time_offset': 60,
                'filters': 0,
                'preview_length': 0,
                'last_message_id': 0
            }
            self.session = self.api.get_api()
        except vk_api.AuthError as error_msg:
            print(error_msg)

    def get_message(self, count=0):
        try:
            response = self.api.method('messages.get', self.values)
            if response['items']:
                self.values['last_message_id'] = response['items'][0]['id']
            return response
        except:
            print('Возникла непредвиденная ошибка. count=%d' % count)
            count += 1
            time.sleep(1)
            if count > 5:
                time.sleep(10)
            return self.get_message(count)

    def respond(self, to, values):
        if 'chat_id' in to:
            values['chat_id'] = to['chat_id']
            self.api.method('messages.send', values)
        else:
            values['user_id'] = to['user_id']
            self.api.method('messages.send', values)

    def mark_as_read(self, message_id):
        values = {
            'message_ids': message_id
        }
        self.api.method('messages.markAsRead', values)

    def get_and_parse_messages(self):
        response = self.get_message()
        for item in response['items']:
            self.parse(item)

    def parse(self, item):
        # print(item)
        self.mark_as_read(item['id'])
        print('> ' + item['body'])
        try:
            if item['body']:
                message = item['body']
                if re.match(r'!p ', message):
                    artist = re.sub(r'!p ', '', message, count=1)
                    print('Sending playlist...')
                    playlist = VkPlaylist(self, item, artist)
                    playlist.send_playlist()
                    print('Playlist sent!')
                    return
                if re.match(r'!s ', message):
                    artist = re.sub(r'!s ', '', message, count=1)
                    print('Sending playlist of similar music...')
                    playlist = VkPlaylist(self, item, artist)
                    playlist.send_playlist(similar=True)
                    print('Playlist sent!')
                    return
                if re.match(r'!help', message):
                    print('Sending help...')
                    message = """
                    *!p название группы* чтобы получить плейлист из 10 популярных треков исполнителя
                    *!s название группы* чтобы получить плейлист содержащий по 2 популярных трека 5 похожих исполнителей
                    *!вов сообщение* или *!c сообщение* для общения с ботом в групповом чате"""
                    self.respond(item, {'message': message})
                    print('Humanitarian aid sent!')
                    return
                if 'chat_id' in item:
                    if re.match(r'!c ', message) or (re.match(r'!вов ', message)):
                        message = re.sub(r'!c |!вов ', '', message, count=1)
                        cb = CleverBot(self, item)
                        cb.exchange_messages(message)
                        return
                    else:
                        return
                cb = CleverBot(self, item)
                cb.exchange_messages(message)
        except:
            self.respond(item, {'message': 'Сожалею, но мне не удалось обработать сообщение.'})
