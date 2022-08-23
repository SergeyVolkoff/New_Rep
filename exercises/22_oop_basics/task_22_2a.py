# -*- coding: utf-8 -*-

"""
Задание 22.2a

Скопировать класс CiscoTelnet из задания 22.2 и изменить
метод send_show_command добавив три параметра:

* parse - контролирует то, будет возвращаться обычный вывод команды или список словарей,
  полученный после обработки с помощью TextFSM.
  При parse=True должен возвращаться список словарей, а parse=False обычный вывод.
  Значение по умолчанию - True.
* templates - путь к каталогу с шаблонами. Значение по умолчанию - "templates"
* index - имя файла, где хранится соответствие между командами и шаблонами.
  Значение по умолчанию - "index"


Пример создания экземпляра класса:

In [1]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [2]: from task_22_2a import CiscoTelnet

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_show_command:
In [4]: r1.send_show_command("sh ip int br", parse=True)
Out[4]:
[{'intf': 'Ethernet0/0',
  'address': '192.168.100.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/1',
  'address': '192.168.200.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/2',
  'address': '192.168.130.1',
  'status': 'up',
  'protocol': 'up'}]

In [5]: r1.send_show_command("sh ip int br", parse=False)
Out[5]: 'sh ip int br\r\nInterface                  IP-Address      OK? Method Status
Protocol\r\nEthernet0/0                192.168.100.1   YES NVRAM  up
up      \r\nEthernet0/1                192.168.200.1   YES NVRAM  up...'


"""


import telnetlib
import yaml

class CiscoTelnet():
    def __init__(self,ip,username,password,secret):
        self.telnet = telnetlib.Telnet(ip)
        self.ip = ip
        self.read_until(b"Username:")
        self.read_until(b"Password:")
        self.read_until(b"Secret:")
        self._write_line(username)
        self._write_line(password)
        self._write_line(secret)
        self._write_line("enable")

    def _write_line(self,line):
        self._write_line(command)
        self.telnet.write(line.encode("ascii") + b"\n")


    def send_show_command(self,command,parse=True,templates,index):
        self._write_line(command)
        command_ouput = self.telnet.read_until(b"#").decode("utf-8")
        return command_ouput

if __name__ == "__main__":
    r1_params = {
      'ip': '192.168.100.1',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco'}
    r1 = CiscoTelnet(**r1_params)
    print(r1.send_show_command("sh ip int bri"))





