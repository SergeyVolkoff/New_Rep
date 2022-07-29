# -*- coding: utf-8 -*-
"""
Задание 21.3

Создать функцию parse_command_dynamic.

Параметры функции:
* command_output - вывод команды (строка)
* attributes_dict - словарь атрибутов, в котором находятся такие пары ключ-значение:
 * 'Command': команда
 * 'Vendor': вендор
* index_file - имя файла, где хранится соответствие между командами и шаблонами.
  Значение по умолчанию - "index"
* templ_path - каталог, где хранятся шаблоны. Значение по умолчанию - "templates"

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br.
"""
import textfsm
from textfsm import clitable

def parse_command_dynamic(command_output, atributes_dict, index_file = "index", templ_path = "templates"):
    clitable1 = clitable.CliTable(index_file, templ_path)
    clitable1.ParseCmd(command_output, atributes_dict)
    return [ dict(zip(clitable1.header,item)) for item in clitable1]
if __name__ == "__main__":
    atributes = {"Command":"sh ip rou o", "Vendor":"cisco_ios"}
    with open("output/sh_ip_route_ospf.txt") as f:
        command_output = f.read()
        print(command_output)
    result_clitable = parse_command_dynamic(command_output, atributes)
    print (result_clitable)
