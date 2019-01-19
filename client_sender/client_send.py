# Клиентская часть

from socket import *
import sys
import time
import json
import argparse
import logging
import inspect
import names
import client_log_config

logger = logging.getLogger('app.main')
user_key = names.get_full_name()


class Log:
    """
    Class of decorator, Used to log functions calls.
    """

    def __init__(self):
        pass

    # Магический метод __call__ позволяет обращаться к
    # объекту класса, как к функции
    def __call__(self, func):
        def decorated(*args, **kwargs):
            whosdaddy = inspect.stack()[1][3]
            res = func(*args, **kwargs)
            logger.debug(
                'Function {} with args {}, kwargs {} = {} was called '
                'from function {}.'.format(
                    func.__name__, args, kwargs, res, whosdaddy)
            )
            return res

        return decorated


@Log()
def arguments():
    """
    Принимает аргументы командной строки [ip, p, v], где:
    ip - адрес сервера, обязателен к вводу.
    p - порт, к которому будет совершено подключение. По умолчанию равен 7777.
    v - уровень логгирования (0=NOTSET, 1=DEBUG, 2=INFO 3=WARNING 4=ERROR 5=CRITICAL), по-умолчанию 2.
    :return: лист, где первым элементом является порт, а вторым - IP для подключения.
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('ip', metavar='<ip>', help='Server IP address', type=str)
    parser.add_argument('-p', default='7777', help='port of remote server', type=int)
    parser.add_argument('-v', default=2, help='verbose level', type=int)
    parsed_opts = parser.parse_args()
    port = parsed_opts.p
    address = parsed_opts.ip
    if parsed_opts.v == 0:
        logger.setLevel(logging.NOTSET)
    elif parsed_opts.v == 1:
        logger.setLevel(logging.DEBUG)
    elif parsed_opts.v == 2:
        logger.setLevel(logging.INFO)
    elif parsed_opts.v == 3:
        logger.setLevel(logging.WARNING)
    elif parsed_opts.v == 4:
        logger.setLevel(logging.ERROR)
    elif parsed_opts.v >= 5:
        logger.setLevel(logging.CRITICAL)
    else:
        # Если уровень логгирования выбран неверно, выводим сообщение и глушим клиент.
        logger.setLevel(logging.CRITICAL)
        logger.critical("UNEXPLAINED COUNT IN VERBOSITY LEVEL!")
        print("UNEXPLAINED COUNT IN VERBOSITY LEVEL!")
        sys.exit()
    logger.info('Попытка коннекта будет осуществлена на адрес {} и порт {}'.format(address, str(port)))
    return [port, address]


@Log()
def make_presence(s, action_key='presence', type_key='status', status_key='I am here!'):
    """
    Создает словарь с ключами action, type, user, затем в формате JSON и кодировке utf-8 отправляет сообщение
    серверу, принимает ответ и выводит его на экран.
    :param s: сокет для соединения
    :param action_key: выполняемое действие, например, presence(статус онлайна) или msg(сообщение).
    :param type_key: тип выполняемого действия
    :param user_key: Имя пользователя
    :param status_key: Статус присутствия
    :return:
    """
    logger.info('The name is ' + user_key)
    msg = {
        'action': action_key,
        'time': int(time.time()),
        'type': type_key,
        'user': {
            'user': user_key,
            'status': status_key
        }
    }
    msg_json = json.dumps(msg)
    s.send(msg_json.encode('utf-8'))
    logger.info('Отправлено сообщение серверу.')
    logger.debug('Содержимое сообщения: {}.'.format(msg))
    data = s.recv(1024)
    logger.info('Получен ответ от сервера.')
    logger.debug('Содержимое ответа: {}.'.format(data.decode('utf-8')))
    print(data.decode('utf-8'))


@Log()
def conv_msg(action_key='message', type_key='msg', msg='Yellow!', status_key='I am here!'):
    """
    Converts user message to JSON format.
    :param action_key: action type, default - message .
    :param type_key: type of action, default is msg.
    :param msg: user message, if not set than uses default Indian Hello version.
    :param status_key: status of user, for future implementation (like Online/Away/Busy).
    :return: dumped into JSON user message
    """
    j_msg = {
        'action': action_key,
        'time': int(time.time()),
        'type': type_key,
        'message': msg,
        'user': {
            'user': user_key,
            'status': status_key
        }
    }
    msg_json = json.dumps(j_msg)
    return msg_json


@Log()
def sock_conn(args):
    """
    Connects client to server.
    :param args: arguments of command line
    :return:
    """
    # При выходе из оператора with сокет будет автоматически закрыт
    with socket(AF_INET, SOCK_STREAM) as sock:  # Создать сокет TCP
        sock.connect((args[1], args[0]))  # Соединиться с сервером
        make_presence(sock, )
        while True:
            msg = input('Your message: ')
            if msg == 'exit':
                break
            elif msg != 'exit':
                msg = conv_msg(msg=msg)
            sock.send(msg.encode('utf-8'))  # Отправить!


# main-функция
def main():
    logger.info('Стартован клиент!')
    args = arguments()
    sock_conn(args)


# Точка входа
if __name__ == '__main__':
    main()
