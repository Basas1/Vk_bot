from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import settings
import time

# Путь к Web Driver
# driver_path = 'C:/Files/Dropbox/Programming/Tools/ChromeDriver/chromedriver.exe'
# driver_path = 'D:/Dropbox/Programming/Tools/ChromeDriver/chromedriver.exe'
# driver_path = 'D:/Dropbox/Programming/Tools/phantomjs-2.1.1-windows/bin/phantomjs.exe'
driver_path = 'C:/Files/Dropbox/Programming/Tools/phantomjs-2.1.1-windows/bin/phantomjs.exe'


class VkPlaylist:
    def __init__(self, vk, item, artist):
        # print(item)
        self.vk = vk
        self.item = item
        self.artist = artist
        print(self.artist)
        self.artist_formated = artist.split()
        self.driver = None
        self.lastfm_url = ''

    # Парсит страницу артиста на сайте last.fm и возвращает список самых популярных композиций этого артиста
    # или 0 в случае, если страницы артиста на данном сайте нет
    def get_top(self, artist):
        artist_url = "&artist=" + artist
        get_top_url = "http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks"
        limit = "&limit=" + "10"
        top_tracks_url = get_top_url + artist_url + settings.lastfm_api_key + limit + "&format=json"
        top_tracks = requests.get(top_tracks_url).json()
        # print(top_tracks)
        tracks = []
        try:
            for i in top_tracks['toptracks']['track']:
                tracks.append(i['name'])
            return tracks
        except:
            return 0

    def fetch_top(self, artist):
        if self.get_top(artist) != 0:
            artist_tracks = {artist: self.get_top(artist)}
            self.lastfm_url = "https://www.last.fm/music/" + "+".join(self.artist_formated)
            return artist_tracks
        else:
            return 0

    # Находит 5 похожих исполнителей и отправляет список самыз популярных треков каждого
    def fetch_similar(self, artist):
        artist_url = "&artist=" + artist
        get_similar_url = "http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar"
        limit = "&limit=" + "5"
        similar_tracks_url = get_similar_url + artist_url + settings.lastfm_api_key + limit + "&format=json"
        similar_tracks = requests.get(similar_tracks_url).json()
        self.lastfm_url = "https://www.last.fm/music/" + "+".join(self.artist_formated) + "/+similar"
        artists = []
        try:
            for i in similar_tracks['similarartists']['artist']:
                artists.append(i['name'])
            artist_tracks = {}
            for j in range(5):
                if self.get_top(artists[j]) != 0:
                    artist_tracks[artists[j]] = self.get_top(artists[j])
            return artist_tracks
        except:
            return 0

    def get_chat_urls(self):
        if 'chat_id' in self.item:
            attach_url = 'https://m.vk.com/attachments?act=choose_audio&target=mail'\
                         + str(2000000000 + int(self.item['chat_id'])) + '&tab=search'
            chat_url = 'https://m.vk.com/mail?act=show&chat=' + str(self.item['chat_id'])
        else:
            attach_url = 'https://m.vk.com/attachments?act=choose_audio&target=mail' + str(
                self.item['user_id']) + '&tab=search'
            chat_url = 'https://m.vk.com/mail?act=show&peer=' + str(self.item['user_id'])
        return attach_url, chat_url

    # Авторизация на сайте vk.com
    def vk_authorization(self, user_login=settings.vk_login, user_password=settings.vk_password):
        self.driver.get('https://m.vk.com/login')
        login = self.driver.find_element_by_name('email')
        login.send_keys(user_login)
        password = self.driver.find_element_by_name('pass')
        password.send_keys(user_password)
        password.send_keys(Keys.RETURN)

    # Прикрепляет аудиозапись "artist - song" к сообщению
    def attach_song(self, artist, song, attach_url):
        self.driver.get(attach_url)
        find_audio = self.driver.find_element_by_class_name('basis__content').find_element_by_name("q")
        find_audio.send_keys(artist + ' - ' + song)
        find_audio.send_keys(Keys.RETURN)
        # time.sleep(1)
        try:
            tc = self.driver.find_element_by_class_name('ai_add')
            add_audio = self.driver.find_elements_by_xpath(
                "//div[@class='audios_block audios_list _si_container']//a[@class='audio_item ai_select']")
            f = 0
            for audio in add_audio:
                at = audio.find_element_by_class_name('ai_title')
                an = audio.find_element_by_class_name('ai_artist')
                if at.text.lower() == song.lower() or at.text.lower() == song.lower() + ' (Original Mix)'.lower() \
                        or at.text.lower() == song.lower() + ' (Original)'.lower():
                    if an.text.lower() == artist.lower():
                        tc = audio.find_element_by_class_name('ai_add')
                        break
                    if f == 0:
                        tc = audio.find_element_by_class_name('ai_add')
                        f = 1
            tc.click()
            return 1
        except:
            print(artist + ' ' + song + ' not found')
            return 0
            pass

    # Поиск песен из плейлиста в аудиозаписях контакта и отправка готового плейлиста пользователю
    def send_playlist1(self, artist, song_names, attach_url, chat_url):
        # Добавление аудиозаписей в прикреплённые к сообщению файлы
        i = 10
        for song in song_names:
            if i == 0:
                break
            t = self.attach_song(artist, song, attach_url)
            if t == 1:
                i -= 1
        # Отправка сообщения пользователю
        self.driver.get(chat_url)
        message = self.driver.find_element_by_xpath("//textarea[@name='message']")
        message.send_keys(self.lastfm_url)
        # message.send_keys('Плейлист "' + artist + '" на основе рейтинга композиций согласно сайту last.fm\n'
        #                   + self.lastfm_url)
        send = self.driver.find_element_by_xpath("//div[@class='cp_buttons_block']//input[@class='button']")
        send.click()

    def send_songs(self, list_of_songs, attach_url, chat_url, number_of_songs):
        # Добавление аудиозаписей в прикреплённые к сообщению файлы
        count_of_attachments = 0
        for artist in list_of_songs:
            if count_of_attachments == 10:
                break
            i = number_of_songs
            for song in list_of_songs[artist]:
                if i == 0:
                    break
                t = self.attach_song(artist, song, attach_url)
                count_of_attachments += 1
                if t == 1:
                    i -= 1
        # Отправка сообщения пользователю
        self.driver.get(chat_url)
        message = self.driver.find_element_by_xpath("//textarea[@name='message']")
        message.send_keys(self.lastfm_url)
        send = self.driver.find_element_by_xpath("//div[@class='cp_buttons_block']//input[@class='button']")
        send.click()

    def send_playlist(self, similar=False):
        if similar:
            list_of_songs = self.fetch_similar(self.artist)
        else:
            list_of_songs = self.fetch_top(self.artist)
        if list_of_songs == 0:
            self.vk.respond(self.item, {'message': 'К сожалению, найти треки исполнителя "'
                                                   + self.artist + '" не удалось.'})
            return
        # print(list_of_songs)
        self.driver = webdriver.PhantomJS(driver_path)
        attach_url, chat_url = self.get_chat_urls()
        self.vk_authorization()
        if len(list_of_songs) != 1:
            self.send_songs(list_of_songs, attach_url, chat_url, 2)
        else:
            self.send_songs(list_of_songs, attach_url, chat_url, 10)
        time.sleep(1)
        self.driver.close()
