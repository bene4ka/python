# Серверная часть

import json
import argparse
from socket import *


def arguments():
    """
    Принимает аргументы командной строки [p, n], где:
    p - порт, по которому будет работать серверный процесс. По умолчанию равен 7777.
    a - адрес интерфейса, на который будет совершен бинд. По умолчанию пуст, что означает бинд на все интерфейсы.
    :return: лист, где первым элементом является порт, а вторым - IP для прослушки.
    """
    parser = argparse.ArgumentParser(description='Collect options.')
    parser.add_argument('-p', default='7777', help='port', type=int)
    parser.add_argument('-a', default='', help='address', type=str)
    parsed_opts = parser.parse_args()
    port = parsed_opts.p
    address = parsed_opts.a
    return [port, address]


def sock_bind(args):
    """"
    Создает TCP-сокет и присваает порт и интерфейс, полученный из функции arguments()
    :param args: лист из порта в integer и адреса интерфейса в string.
    """
    s = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP
    s.bind((args[1], args[0]))        # Присваивает порт 8888
    s.listen(5)                       # Переходит в режим ожидания запросов, одновременно не болеее 5 запросов
    return s


def receiver(data):
    """
    Получает принятые данные и анализирует. Если это presence сообщение от залогинившегося пользователя, посылает ему
    приветственное сообщение. Т.к. никакой другой функционал JIM еще не организован, если это не presence,
    вернется ответ о ошибочном действии.
    :param data: JSON, принятый от клиента.
    :return: ответ клиенту в формате string.
    """
    if data.get('action') == 'presence':
        resp = 'You are online!'
    else:
        resp = 'Error action, pal.'
    return resp


def listen(s):
    """
    Бесконечный цикл, ожидает сообщения от клиента, передает их в декодированном виде в receiver(), для анализа и
    соответствующего действию ответа.
    :param s: сокет, созданный в функции sock_bind
    """
    while True:
        client, addr = s.accept()
        data_json = client.recv(1000000)
        if not data_json:
            break
        data = json.loads(data_json.decode('utf-8'))
        print('Пришло сообщение: ', data, ', от клиента: ', addr)
        respond = receiver(data)
        client.send(respond.encode('utf-8'))
        client.close()


# main-функция
def main():
    args = arguments()
    s = sock_bind(args)
    listen(s)


# Точка входа
if __name__ == '__main__':
    main()
