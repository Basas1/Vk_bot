from get_playlist import VkPlaylist
from cleverbot_api import CleverBot
import re


def parse(vk, item):
    # print(item)
    vk.mark_as_read(item['id'])  # Помечаем прочитанным
    print('> ' + item['body'])
    try:
        if item['body']:
            message = item['body']
            if re.match(r'!p ', message):
                artist = re.sub(r'!p ', '', message, count=1)
                print('Sending playlist...')
                playlist = VkPlaylist(vk, item, artist)
                playlist.send_playlist()
                print('Playlist sent!')
                return
            if re.match(r'!s ', message):
                artist = re.sub(r'!s ', '', message, count=1)
                print('Sending playlist of similar music...')
                playlist = VkPlaylist(vk, item, artist)
                playlist.send_playlist(similar=True)
                print('Playlist sent!')
                return
            if 'chat_id' in item:
                if re.match(r'!c ', message) or (re.match(r'!вов ', message)):
                    message = re.sub(r'!c |!вов ', '', message, count=1)
                    cb = CleverBot(vk, item)
                    cb.exchange_messages(message)
                    return
                else:
                    return
            cb = CleverBot(vk, item)
            cb.exchange_messages(message)
        # if 'emoji' in item:
        #     vk.respond(item, {'message': 'СМАЙЛИК! xD'})
    except:
        vk.respond(item, {'message': 'Некорректное сообщение. Попробуйте ещё раз.'})

