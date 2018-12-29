# Программа сервера времени
from socket import *
import time
import unittest


def create_socket():
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('', 8888))
    s.listen(5)
    return s


def listener(s):
    while True:
        client, addr = s.accept()
        print("Получен запрос на соединение от %s" % str(addr))
        timestr = (time.ctime(time.time()) + "\n").encode('ascii')
        client.send(timestr)
        client.close()
        break  # для того, чтобы прервать выполнения кода после 1 тестового запроса от клиента
    return timestr


#
# > UNITTEST SECTION <
#
class TestTimeSender(unittest.TestCase):
    sock = create_socket()
    timestr = listener(sock)

    def test_var_presence(self):
        self.assertTrue(self.__class__.timestr)

    def test_if_bytes(self):
        self.assertIsInstance(self.__class__.timestr, bytes)

    def test_decoding(self):
        def decoding():
            return self.__class__.timestr.decode('ascii')
        self.assertRaises(UnicodeDecodeError, decoding)

    def test_if_not_bytes(self):
        self.assertIsInstance(self.__class__.timestr, str)


if __name__ == '__main__':
    unittest.main()
