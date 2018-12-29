# Программа вывода сообщений на стороне сервера при запросе от клиента
from socket import *
import unittest


def create_socket():
    s = socket(AF_INET, SOCK_DGRAM)  # Определяем UDP-протокол
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Несколько приложений может слушать сокет
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)  # Определяем широковещательные пакеты
    s.bind(('', 8888))
    return s


def listener(s):
    while True:
        msg = s.recv(128)
        break
    return msg


#
# > UNITTEST SECTION <
#
class TestDataServer(unittest.TestCase):
    s = create_socket()
    msg = listener(s)

    def test_data_received(self):
        self.assert_(self.__class__.msg)


if __name__ == '__main__':
    unittest.main()