import time
from vk_login import VkConnect
import settings
import message_parse


def get_message(vk, count=0):
    values = {
        'out': 0,
        'offset': 0,
        'count': 20,
        'time_offset': 50,
        'filters': 0,
        'preview_length': 0,
        'last_message_id': lastmessid
    }
    try:
        response = vk.api.method('messages.get', values)
        return response
    except:
        print('Возникла непредвиденная ошибка.')
        count += 1
        if count > 5:
            print('Непредвиденные ошибки привели к остановке программы.')
            return 0
        return get_message(vk, count)


def main():
    global lastmessid
    lastmessid = 0
    print('Бот Владимир запущен!')
    print('Авторизация в вк...')
    vk = VkConnect(settings.vk_login, settings.vk_password, settings.vk_app_id)
    print('Приступаю к приему сообщений')

    while True:
        response = get_message(vk)
        if response['items']:
            lastmessid = response['items'][0]['id']
            for item in response['items']:
                message_parse.parse(vk, item)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
