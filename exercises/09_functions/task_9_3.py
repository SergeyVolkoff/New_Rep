# -*- coding: utf-8 -*-
"""
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный
файл коммутатора и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов,
  а значения access VLAN (числа):
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов,
  а значения список разрешенных VLAN (список чисел):
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент
имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""


def get_int_vlan_map (config_filename):
    intf_acc_vlan = {}
    intf_trunk_vlan = {}
    with open(config_filename) as conf:
        for line in conf:
            line = line.strip()
            if line.startswith("interface"):
                    interfacic = line.split()[1]
            elif "access vlan" in line:
                    intf_acc_vlan[interfacic]= int(line.split()[-1])
            elif "trunk allowed" in line:
                    intf_trunk_vlan[interfacic]=[int(val) for val in line.split()[-1].split(",")]
        return intf_acc_vlan, intf_trunk_vlan


