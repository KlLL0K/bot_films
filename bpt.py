from main import BASE_URL, TOKEN
import requests


def pulling():
    count_message = 0
    while True:
        response = requests.get(f'{BASE_URL}{TOKEN}/getUpdates').json()
        if count_message != len(response['result']):
            count_message = len(response['result'])
            message = response['result'][-1]
            file_id = message['message']['video']['file_id']
            user_id = message['message']['from']['id']
            requests.post(f'{BASE_URL}{TOKEN}/',
                          json={'method': 'sendMessage', 'chat_id': f"{user_id}", "text": "Обычная клавиатура",
                                'reply_markup': {'keyboard': [[{'test': 'yes'}, {'test': 'no'}]],
                                                'resize_keyboard': True, 'one_time_keyboard': True},
                                })


pulling()
