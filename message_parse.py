from get_playlist import VkPlaylist


def clean(message):
    rem = {".", ",", "?", "!", "#", "$", "%", "&", "*", ":", '"'}
    s = message
    for i in range(len(s)):
        if s[i] in rem:
            s = s[:i] + s[i + 1:]
            s = clean(s)
            break
    return s


def parse_message(vk, item):
    print(item)
    vk.mark_as_read(item['id'])  # Помечаем прочитанным
    print('> ' + item['body'])
    try:
        if item['body']:
            words = clean(item['body']).split()
            if words[0] == '@p':
                z = ""
                for i in words:
                    if i == "@p":
                        continue
                    z = z + ' ' + i
                artist = z[1:]
                print('ОТПРАВЛЯЮ PLAYLIST!')
                VkPlaylist(vk, item, artist)
                print('ОТПРАВИЛ!')
        try:
            if item['emoji'] == 1:
                vk.respond(item, {'message': 'НАХЕРА ТЫ МНЕ СМАЙЛЫ ШЛЁШЬ, ИДИОТ? Я ВСЕГО ЛИШЬ БОТ.'
                                             ' Я НЕ ВОСПРИНИМАЮ ЭТО ГОВНО.'})
        except:
            pass
    except:
        vk.respond(item, {'message': 'Некорректное сообщение. Попробуйте ещё раз.'})
