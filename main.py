# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time
from urllib.request import urlopen


def print_hi(name):
    import base64
    import socket
    import ssl
    from pathlib import Path
    mime = {}
    mime['image'] = ['image/bmp', 'image/gif', 'image/jpeg', 'image/png',
                     'image/webp']
    mime['text'] = ['text/plain', 'text/calendar', 'text/html', 'text/css',
                    'text/javscript']
    mime['application'] = ['application/gzip', 'application/json']
    mime['video'] = ['video/mpeg']
    if not connect():
        return

    def request(socket, request):
        socket.send((request + '\n').encode())
        recv_data = socket.recv(65535).decode()
        return recv_data

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(('smtp.yandex.ru', 465))
        client = ssl.wrap_socket(client)
        client.recv(1024).decode()
        request(client, 'ehlo myUserName')

        base64login = base64.b64encode(
            ''.encode()).decode()
        base64password = base64.b64encode(''.encode()).decode()

        request(client, 'AUTH LOGIN')
        request(client, base64login)

        req = request(client, base64password)
        if int(req.split()[0]) == 535:
            print('Повторите ввод логина и пароля,одно из полей некорректно')
            return
        else:
            print('Авторизация прошла успешно')
            time.sleep(0.3)
        sender = request(client, 'MAIL FROM:kondrat007007@yandex.ru')
        if int(sender.split()[0]) == 553:
            print(
                'Повторите ввод отправителя,значение поля не соответствует логину авторизованного пользователя')
            return
        else:
            print('Адрес отправителя корректен')
            time.sleep(0.3)
        adress = request(client, "RCPT TO:kondrat007007@yandex.ru")
        if int(adress.split()[0]) == 504:
            print('Повторите ввод получателя,значение поля некорректно')
            return
        elif int(adress.split()[0]) == 555:
            print('Поле получателя пусто')
            return
        else:
            print('Адрес получателя корректен')
            time.sleep(0.3)
        request(client, 'DATA')

        msg = ''

        with open('headers.txt') as f:
            msg += f.readline()
            msg += f.readline()
            msg += f.readline().encode('cp1251').decode()
            msg += f.readline()

        msg += '\n'

        bound = '--my-bound-mix'

        msg += 'Content-Type: multipart/mixed;' + \
               f'boundary="{bound}"'

        msg += '\n\n'
        msg += f'--{bound}\n'
        msg += f'Content-Type: {mime["text"][0]}\n\n'

        msg += open('msg.txt').read() + '\n'
        for f in Path('./attachments').iterdir():
            msg += f'--{bound}\n'

            msg += 'Content-Disposition: attachment;\n' + \
                   f' filename="{f.name}"\n'
            msg += 'Content-Transfer-Encoding: base64\n'
            msg += f'Content-Type: {mime["image"][2]}'
            msg += '\n\n'

            with f.open('rb') as f1:
                msg += base64.b64encode(f1.read()).decode()

            msg += '\n'

        msg += f'--{bound}--'
        msg += '\n.\n'
        print(msg)
        result = request(client, msg)
        if int(result.split()[0]) == 250:
            print('Отправка прошла успешно!')

        else:
            print('Упс, что-то пошло не так!')


def connect():
    try:
        urlopen('http://google.com')
        return True
    except:
        print("нет соединения")
        return False


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
