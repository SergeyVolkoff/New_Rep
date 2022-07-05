# -*- coding: utf-8 -*-
"""
Задание 18.1b

Скопировать функцию send_show_command из задания 18.1a и переделать ее таким образом,
чтобы обрабатывалось не только исключение, которое генерируется при ошибке
аутентификации на устройстве, но и исключение, которое генерируется, когда IP-адрес
устройства недоступен.

При возникновении ошибки, на стандартный поток вывода должно выводиться
сообщение исключения.

Для проверки измените IP-адрес на устройстве или в файле devices.yaml.
"""
from pprint import pprint
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


def send_show_command(device, command):
    result = ''
    try:
        with ConnectHandler(**device)as ssh:
            result = ssh.send_command(command)
        return result
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print("*"*20, "error","*"*20)


if __name__ == "__main__":
    command = "ifconfig"
    with open("device2.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        print(send_show_command(dev, command))
