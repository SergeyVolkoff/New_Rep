# -*- coding: utf-8 -*-
"""
Задание 18.2a

Скопировать функцию send_config_commands из задания 18.2 и добавить параметр log,
который контролирует будет ли выводится на стандартный поток вывода информация о том
к какому устройству выполняется подключение.
По умолчанию, результат должен выводиться.

Пример работы функции:

In [13]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...

In [14]: result = send_config_commands(r1, commands, log=False)

In [15]:

Скрипт должен отправлять список команд commands на все устройства
из файла devices.yaml с помощью функции send_config_commands.
"""
from pprint import pprint
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


def send_config_commands(device, config_commands, log = True):
    if log:
        print(f"Connect to {device['host']}...")
    try:
        result = ""
        with ConnectHandler(**device) as ssh:
            result = ssh.send_config_set(config_commands)
        return result
    except netmiko.NetmikoAuthenticationException as error:
        print("*"*20, "AuthenticationError","*"*20)
    except netmiko.NetmikoTimeoutException as error:
        print("*"*20, "TimeoutException","*"*20)

if __name__ == "__main__":
    commands = ["ifconfig | grep eth0","uci show | grep '127.0.0.1'"]
    with open ("device2.yaml") as f:
        devices = yaml.safe_load(f)
    for dev in devices:
         print(send_config_commands(dev,commands))
