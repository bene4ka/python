# Клиентская часть

from socket import *
import sys
import argparse
import logging
import inspect
import client_log_config

logger = logging.getLogger('app.main')


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
    parser.add_argument('ip', default='127.0.0.1', metavar='<ip>', help='Server IP address', type=str)
    parser.add_argument('-p', default='7777', help='port of remote server', type=int)
    parser.add_argument('-v', default=1, help='verbose level', type=int)
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
def sock_conn(args):
    """
    Connects receiver client to server
    :param args: arguments of command line
    :return:
    """
    with socket(AF_INET, SOCK_STREAM) as sock:  # Создать сокет TCP
        sock.connect((args[1], args[0]))  # Соединиться с сервером
        while True:
            data = sock.recv(1024).decode('utf-8')
            print(data)


# main-функция
def main():
    logger.info('Стартован клиент!')
    args = arguments()
    sock_conn(args)


# Точка входа
if __name__ == '__main__':
    main()
