import unittest


def byte_row_to_unicode_row(bs):
    return bs.decode('cp1251')


def unicode_row_to_byte_row(s):
    return s.encode('koi8-r')


def unicode_row_to_byte_massive(s):
    return bytearray(s, 'utf-8')


# В Python 3 все строки - строки юникода
s = 'Python'

# Отдельный тип - строка байтов
bs = b'Python'

# Отдельный тип - bytearray - изменяемая строка байтов
ba = bytearray(bs)

# Преобразования между строками
s2 = byte_row_to_unicode_row(bs)  # Из байт-строки в юникод строку
bs2 = unicode_row_to_byte_row(s)  # Из юникод-строки в строку байтов

ba2 = unicode_row_to_byte_massive(s)  # Из юникод-строки в массив байтов


#
# > UNITTEST SECTION <
#
class TestArrays(unittest.TestCase):
    # Тесты с верными результатами
    def test_br_to_ur(self):
        self.assertEqual(byte_row_to_unicode_row(b'Python'), 'Python', 'Возвращена не юникод строка')

    def test_ur_to_br(self):
        self.assertEqual(unicode_row_to_byte_row('Python'), b'Python', 'Возвращена не байтовая строка')

    def test_ur_to_bm(self):
        self.assertEqual(unicode_row_to_byte_massive('Python'), bytearray(b'Python'), 'Возвращен не массив байтов')

    # Тесты с неверными результами
    def test_br_to_ur2(self):
        self.assertEqual(byte_row_to_unicode_row(b'Python'), b'Python', 'Возвращена не байтовая строка')

    def test_ur_to_br2(self):
        self.assertEqual(unicode_row_to_byte_row('Python'), 'Python', 'Возвращена не юникод строка')

    def test_ur_to_bm2(self):
        self.assertEqual(unicode_row_to_byte_massive('Python'),
                         bytearray('Python', 'utf-16'), 'Возвращен не массив байтов в utf-16')


if __name__ == '__main__':
    unittest.main()
