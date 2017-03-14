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
                artist = re.findall(r'!p (.*)', message)[0]
                print('Sending playlist...')
                playlist = VkPlaylist(vk, item, artist)
                playlist.send_playlist()
                print('Playlist sent!')
                return
            if re.match(r'!s ', message):
                artist = re.findall(r'!s (.*)', message)[0]
                print('Sending playlist of similar music...')
                playlist = VkPlaylist(vk, item, artist)
                playlist.send_playlist(similar=True)
                print('Playlist sent!')
                return
            if 'chat_id' in item:
                if re.match(r'!c ', message) or (re.match(r'!вов ', message)):
                    message = re.findall(r'!c (.+)|!вов (.+)', message)[0]
                    # print(message)
                    for i in message:
                        if i:
                            message = i
                            break
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

