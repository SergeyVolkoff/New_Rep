# -*- coding: utf-8 -*-
"""
Задание 17.3

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
"""
import re
import csv

def parse_sh_cdp_neighbors(cfg_neib):
    regex = re.compile(
    r"(?P<nei_dev>\w+)  +(?P<loc_intf>\S+ \S+)"
    r"  +\d+  +(\w ){3} +\S+ +(?P<nei_intf>\S+ \S+)"
    )
    result={}
    dev=re.search(r"(\S+)[>]", cfg_neib).group(1)

    result[dev]={}
    match = re.search(regex, cfg_neib)
    for match in regex.finditer(cfg_neib):
        nei_dev, loc_intf, nei_intf = match.group("nei_dev", "loc_intf", "nei_intf")
        result[dev][loc_intf] ={nei_dev : nei_intf}

    return result

if __name__=="__main__":
    with open("sh_cdp_n_sw1.txt")  as f:
     print(parse_sh_cdp_neighbors(f.read()))
