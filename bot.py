import time
from vk_interactions import Vk
import settings
# kek
# kek sas joj

def main():
    print('Бот Владимир запущен!')
    print('Авторизация в вк...')
    bot = Vk(settings.vk_login, settings.vk_password)
    print('Приступаю к приему сообщений')

    while True:
        bot.get_and_parse_messages()
        time.sleep(0.5)

if __name__ == '__main__':
    main()
