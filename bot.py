import time
from vk_login import VkConnect
import settings
import message_parse


def main():
    print('Бот Владимир запущен!')
    print('Авторизация в вк...')
    vk = VkConnect(settings.vk_login, settings.vk_password)
    print('Приступаю к приему сообщений')

    while True:
        response = vk.get_message()
        for item in response['items']:
            message_parse.parse(vk, item)
        time.sleep(0.5)

if __name__ == '__main__':
    main()
