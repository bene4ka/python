# Программа клиента, запрашивающего текущее время
from socket import *
import unittest


def create_socket():
    s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
    s.connect(('localhost', 8888))  # Соединиться с сервером
    return s


def recieve_time(s):
    tm = s.recv(1024)  # Принять не более 1024 байтов данных
    s.close()
    current_time = tm.decode('ascii')
    print("Текущее время: %s" % current_time)
    return current_time


#
# > UNITTEST SECTION <
#
class TestTimeReceiver(unittest.TestCase):
    s = create_socket()
    time = recieve_time(s)

    # Тесты с верными результатами
    def test_time_presence(self):
        self.assert_(self.__class__.time)

    def test_time_isinstance(self):
        self.assertIsInstance(self.__class__.time, str)

    def test_year_in_time(self):
        self.assert_('2018' in self.__class__.time)

    # Тесты с неверными результатами
    def test_time_presence2(self):
        self.failIf(self.__class__.time)

    def test_time_isinstance2(self):
        self.assertIsInstance(self.__class__.time, int)

    def test_year_in_time2(self):
        self.assert_('2017' in self.__class__.time)


if __name__ == '__main__':
    unittest.main()
