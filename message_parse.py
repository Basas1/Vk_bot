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
            if re.match(r'!p ', message) or re.match(r'@p ', message):
                artist = re.findall(r'!p (.*)|@p (.*)', message)[0]
                for i in artist:
                    if i:
                        artist = i
                        break
                print('Sending playlist...')
                VkPlaylist(vk, item, artist)
                print('Playlist sent!')
                return
            if 'chat_id' in item:
                if re.match(r'!c ', message) or (re.match(r'!вов ', message)):
                    message = re.findall(r'!c (.*)|!вов (.*)', message)[0]
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

