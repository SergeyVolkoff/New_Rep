# -*- coding: utf-8 -*-
"""
Задание 18.1a

Скопировать функцию send_show_command из задания 18.1 и переделать ее таким образом,
чтобы обрабатывалось исключение, которое генерируется при ошибке аутентификации
на устройстве.

При возникновении ошибки, на стандартный поток вывода должно выводиться
сообщение исключения.

Для проверки измените пароль на устройстве или в файле devices.yaml.
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
    except netmiko.NetmikoAuthenticationException as error:
        print("*"*20, "AuthenticationError","*"*20)


if __name__ == "__main__":
    command = "ifconfig"
    with open("device2.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        print(send_show_command(dev, command))
