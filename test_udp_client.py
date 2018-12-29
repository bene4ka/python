# Программа клиента, передающего серверу сообщения при каждом запросе на соединение
from socket import *
import unittest


def create_socket():
    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    return s


def sender(s):
    while True:
        s.sendto(b'request!', ('localhost', 8888))
        break


#
# > UNITTEST SECTION <
#
class TestDataServer(unittest.TestCase):
    s = create_socket()
    sender(s)
    def test_connect(self):
        self.assertRaises(ConnectionError, sender())


if __name__ == '__main__':
    unittest.main()
