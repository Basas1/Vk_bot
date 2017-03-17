import vk_api
import time


class VkConnect:
    api = None

    def __init__(self, login, password):
        try:
            self.api = vk_api.VkApi(login, password)
            self.api.authorization()
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
        except vk_api.AuthorizationError as error_msg:
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

    def mark_as_read(self, id):
        values = {
            'message_ids': id
        }
        self.api.method('messages.markAsRead', values)
