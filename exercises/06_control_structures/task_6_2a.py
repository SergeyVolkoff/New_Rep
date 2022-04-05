# -*- coding: utf-8 -*-
"""
Задание 6.2a

Сделать копию скрипта задания 6.2.

Добавить проверку введенного IP-адреса.
Адрес считается корректно заданным, если он:
   - состоит из 4 чисел (а не букв или других символов)
   - числа разделенны точкой
   - каждое число в диапазоне от 0 до 255

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'

Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
in_ipaddress = input("Input ip in format xx.xx.xx.xx= ")

all_octets = in_ipaddress.split('.')
valid_ip = len(all_octets) == 4

for o in all_octets:
     valid_ip = o.isdigit() and 0<=int(o)<=255 and valid_ip

if valid_ip == True:
    if 1<=int(all_octets[0])<=223:
        print('unicast')
    elif 224<=int(all_octets[0])<=239:
        print('multicast')
    elif in_ipaddress == "255.255.255.255":
        print('local broadcast')
    elif in_ipaddress == "0.0.0.0":
        print('unassigned')
    else:
        print('unused')
else:
    print("Неправильный IP-адрес")

