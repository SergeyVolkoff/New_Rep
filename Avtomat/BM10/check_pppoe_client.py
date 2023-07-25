import re
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from clss_Router import Router

'''
Проверяем работу роутера как РРРоЕ клиента:

'''
with open("BM10_LTE.yaml") as f:
    temp = yaml.safe_load(f)
    for t in temp:
        device = dict(t)
        r1 = Router(**device)

def check_int_pppoe_cl(comm):  # Определяем наличие настроенного интерфейса ван с РРРоЕ (есть ли конфиг вообще)
    try:
        temp = r1.send_sh_command(device, comm)
        if "pppoe" in temp:
            return True
        else:
            return False
    except ValueError as err:
        return False
def check_ip_pppoe(comm): # check ip for client and serv
    try:
        temp = r1.send_sh_command(device,comm)
        temp2 = re.search(r'\s+inet (?P<intf>\d+.\d+.\d+.\d+) peer (.{0,})pppoe-wan',temp).group()
        output = re.search(r'\s+inet (?P<ip_int>\d+.\d+.\d+.\d+) peer (?P<ip_peer>\d+.\d+.\d+.\d+).{0,}pppoe-wan', temp)
        #ip_per=output.group('ip_peer')
        if "inet" in temp2:
            print('Tunnel ok, ip client:',output.group('ip_int'),', ip peer(serv):',output.group('ip_peer'))
            return True
        else:
            if "state DOWN"in temp2:
                print("interface exist, but state DOWN")
                return False
    except ValueError as err:
        return False

def check_ping_inet(): # check ping Internet
    r1.ip_for_ping = "8.8.8.8"
    try:
        res_ping_inet = r1.ping_ip(device,r1.command_ping)
        print(res_ping_inet)
        if "destination available" in res_ping_inet:
            print("Inet(8.8.8.8) availeble, PPPoE OK")
            return True
        else:
            print("Inet(8.8.8.8)- not available, PPPoE bad ")
            return False
    except ValueError as err:
        return False
def check_ip_peer(comm): # retutn ip serv for test with Task
    try:
        temp = r1.send_sh_command(device,comm)
        output = re.search(r'\s+inet (?P<ip_int>\d+.\d+.\d+.\d+) peer (?P<ip_peer>\d+.\d+.\d+.\d+).{0,}pppoe-wan', temp)
        ip_per=output.group('ip_peer')
        return ip_per
    except ValueError as err:
        return False
if __name__ =="__main__":
    result = check_ip_peer("ip a")
    print (type(result))

