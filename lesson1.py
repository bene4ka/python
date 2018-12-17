import subprocess
import chardet

# 1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и содержание
# соответствующих переменных. Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode
# и также проверить тип и содержимое переменных.
print('\n== TASK 1 ===============================================================================')

devel = 'разработка'
sock = 'сокет'
decor = 'декоратор'

print(devel, sock, decor)
print(type(devel), type(sock), type(decor), '\n')

devel_u = '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430'
sock_u = '\u0441\u043e\u043a\u0435\u0442'
decor_u = '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'

print(devel_u, sock_u, decor_u)
print(type(devel_u), type(sock_u), type(decor_u), '\n\n')


# 2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов
# (не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.
print('\n == TASK 2 ===============================================================================')

cl = b'class'
fn = b'function'
mt = b'method'

print(type(cl), type(fn), type(mt))
print(cl, fn, mt)
print(len(cl), len(fn), len(mt), '\n')


# 3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
print('\n== TASK 3 ===============================================================================')

attr = b'attribute'
print("""
Нельзя записать в байтовом виде, потому что байты могут содержать только ASCII: 
cl = b'класс'
fn = b'функция' """)

tp = b'type'


# 4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в
# байтовое и выполнить обратное преобразование (используя методы encode и decode).
print('\n== TASK 4 ===============================================================================')

adm = 'администрирование'
prot = 'protocol'
stand = 'standard'

devel_encoded = devel.encode('utf-8')
adm_encoded = adm.encode('utf-8')
prot_encoded = prot.encode('utf-8')
stand_encoded = stand.encode('utf-8')

print(devel_encoded, adm_encoded, prot_encoded, stand_encoded)

devel_decoded = devel_encoded.decode('utf-8')
adm_decoded = adm_encoded.decode('utf-8')
prot_decoded = prot_encoded.decode('utf-8')
stand_decoded = stand_encoded.decode('utf-8')

print(devel_decoded, adm_decoded, prot_decoded, stand_decoded)


# 5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в строковый тип
# на кириллице.
print('\n== TASK 5 ===============================================================================')

args = ['ping', 'yandex.ru']
subproc_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
for line in subproc_ping.stdout:
    line = line.decode('cp866').encode('utf8')
    print(line.decode('utf-8'))

args = ['ping', 'youtube.com']
subproc_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
for line in subproc_ping.stdout:
    line = line.decode('cp866').encode('utf8')
    print(line.decode('utf-8'))


# 6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет»,
# «декоратор». Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести
# его содержимое.
print('\n== TASK 6 ===============================================================================')

file = open('test_file.txt', 'w')
file.write('сетевое программирование\nсокет\nдекоратор')
file.close()

detector = chardet.UniversalDetector()
with open('test_file.txt', 'rb') as fh:
    for line in fh:
        detector.feed(line)
        if detector.done:
            break
    detector.close()
print(detector.result)

try:
    with open('test_file.txt', encoding='utf-8') as fh:
        for line in fh:
            print(line.decode('windows-1251').encode('utf-8'))
except:
    print('Кодировка файла отличается от UTF-8, файл открыть не удалось')
