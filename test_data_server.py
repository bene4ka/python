# Программа сервера для получения приветствия от клиента и отправки ответа
from socket import *
import unittest


def create_socket():
    s = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP
    s.bind(('', 8007))  # Присваивает порт 8888
    s.listen(5)  # Переходит в режим ожидания запросов;
    # Одновременно обслуживает не более
    # 5 запросов.
    return s


def listener(s):
    while True:
        client, addr = s.accept()
        data = client.recv(1000000)
        print('Сообщение: ', data.decode('utf-8'), ', было отправлено клиентом: ', addr)
        msg = 'Привет, клиент'
        client.send(msg.encode('utf-8'))
        client.close()
        break
    return data


#
# > UNITTEST SECTION <
#
class TestDataServer(unittest.TestCase):
    s = create_socket()
    data = listener(s)

    def test_data_received(self):
        self.assert_(self.__class__.data)

    def test_data_decoding(self):
        def decode_data():
            return self.__class__.data.decode('utf-8')

        self.assertRaises(UnicodeDecodeError, decode_data())


if __name__ == '__main__':
    unittest.main()
