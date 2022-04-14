# -*- coding: utf-8 -*-
"""
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Переделать скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Пример работы скрипта:

Enter VLAN number: 10
10       0a1b.1c80.7000      Gi0/4
10       01ab.c5d0.70d0      Gi0/8

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
number_vlan = input("Input number of vlan = ")

result = []

with open("CAM_table.txt") as f:
    for line in f:
        fragment = line.split()
        #print(fragment)

        if fragment and fragment[0].isdigit() and fragment[0] == number_vlan:
            vlan, mac, typ, interface = fragment
            result.append([int(vlan), mac, interface])

    for vlan, mac, intf in result:
        print(f"{vlan:<9}{mac:20}{intf}")



