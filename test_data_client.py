# Программа клиента для отправки приветствия серверу и получения ответа
from socket import *
import unittest


def create_socket():
    try:
       s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
       s.connect(('localhost', 8007))  # Соединиться с сервером
    except ConnectionRefusedError:
        s = None
    return s


def talk_with(s):
    try:
        msg = 'Привет, сервер'
        s.send(msg.encode('utf-8'))
        data = s.recv(1000000)
        print('Сообщение от сервера: ', data.decode('utf-8'), ', длиной ', len(data), ' байт')
        s.close()
    except AttributeError:
        data = 'Connection Error'
    return data


#
# > UNITTEST SECTION <
#
class TestDataClient(unittest.TestCase):
    s = create_socket()
    data = talk_with(s)
    print(data)

    def test_connection(self):
        self.assertTrue(self.__class__.s == None)

    def test_data_bytes(self):
        self.assertIsInstance(self.__class__.data, bytes)


if __name__ == '__main__':
    unittest.main()