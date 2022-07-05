# -*- coding: utf-8 -*-
"""
Задание 18.1

Создать функцию send_show_command.

Функция подключается по SSH (с помощью netmiko) к ОДНОМУ устройству
и выполняет указанную команду.

Параметры функции:
* device - словарь с параметрами подключения к устройству
* command - команда, которую надо выполнить

Функция возвращает строку с выводом команды.

Скрипт должен отправлять команду command на все устройства из файла devices.yaml
с помощью функции send_show_command (эта часть кода написана).

"""
from pprint import pprint
import yaml
import netmiko
from netmiko import ConnectHandler


def send_show_command(device, command):
    result = ''
    with ConnectHandler(**device) as ssh:
        result = ssh.send_command(command)
    return result



if __name__ == "__main__":
    command = "ifconfig"
    with open("device2.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        print(send_show_command(dev, command))
