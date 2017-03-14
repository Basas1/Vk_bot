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
                artist = re.findall('!p (.*)', message)[0]
                print('Sending playlist...')
                VkPlaylist(vk, item, artist)
                print('Playlist sent!')
                return
            if 'chat_id' in item:
                if re.match(r'!c ', message) or (re.match(r'!вов ', message)):
                    cb = CleverBot(vk, item)
                    cb.exchange_messages(message)
                    return
                else:
                    return 
            cb = CleverBot(vk, item)
            cb.exchange_messages(message)
        # if 'emoji' in item:
        #     vk.respond(item, {'message': 'НАХЕРА ТЫ МНЕ СМАЙЛЫ ШЛЁШЬ, ИДИОТ? Я ВСЕГО ЛИШЬ БОТ.'
        #                                      ' Я НЕ ВОСПРИНИМАЮ ЭТО ГОВНО.'})
    except:
        vk.respond(item, {'message': 'Некорректное сообщение. Попробуйте ещё раз.'})

