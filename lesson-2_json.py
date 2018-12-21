#
# Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах.
# Написать скрипт, автоматизирующий его заполнение данными. Для этого:
# Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity),
# цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря в файл
# orders.json. При записи данных указать величину отступа в 4 пробельных символа;
# Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
#

import json


def write_order_to_json(item, quantity, price, buyer, date):
    """Функция составляет словарь из входных данных, затем открывает файл order.json и считывает уже внесенные
    в файл данные, сохраняя их, чтобы потом сделать append новых данных. После append словарь записывается
    в файл.
    """

    # Словарь полученных функцией аргументов.
    dict_to_json = {
        "item": item,
        "quantity": quantity,
        "price": price,
        "buyer": buyer,
        "date": date
    }

    # Открывается файл JSON и в переменную считывается уже имеющаяся информация.
    with open('orders.json') as data_file:
        old_data = json.load(data_file)

    # Создается список словарей с старыми значениями, затем добавляется новый словарь.
    list_of_dicts = old_data.get('orders')
    list_of_dicts.append(dict_to_json)

    # Составляется результирующий набор данных для записи в JSON-файл.
    new_data = {'orders': list_of_dicts}

    # Результирующий набор записывается в файл с отступом в 4 символа.
    with open('orders.json', 'w') as f_n:
        json.dump(new_data, f_n, indent=4)

# Main-функция, запускающая функцию write_order_to_json с аргументами.
def main():
    write_order_to_json('apple','1','100','Vasya','11-11-1008')

# Точка входа.
if __name__ == '__main__':
    main()