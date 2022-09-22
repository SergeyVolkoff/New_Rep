 # Создать функцию для настройки и проверки интерфейса wwan0.
import re
import pexpect
from pprint import pprint
from show_int34_netmiko import send_show_command
from cfg_int34_BM10 import cfg_wwan_BM10
import time
from ping import ping_ip


result_def_show = send_show_ifcof("192.168.1.1", "root", "root")

if 'addr:' in result_def_show:
    def ping_ip(ip_s, ip_dest, user, password):
        result=""
        with pexpect.spawn(f"ssh {user}@{ip_s}", timeout=10, encoding="utf-8") as ssh:
            ssh.expect("d:")
            ssh.sendline(password)
            ssh.expect("root@BWOS:~#")

            ssh.send("ping ")
            ssh.send(ip_dest)
            ssh.sendline(" -w 1")
            ssh.expect("root@BWOS:~#")
            temp = ssh.before
            if "round-trip min/avg/max" in temp:
                temp = re.search(r'round-trip min/avg/max = (\S+ ..)', temp).group()
                result += temp
                print("*"*30)
                print("IP ",ip_dest, "destination  available from 3G: ",result)
            else:
                print("*"*30)
                print("Ip ",ip_dest, "out of destination")
        return result
else:
    cfg_commands = [
    "uci set network.34G=interface",
    "uci set network.34G.proto='qmi'",
    "uci set network.34G.device='/dev/cdc-wdm0'",
    "uci set network.34G.apn='internet.tele2.ru'",
    "uci set network.34G.pdptype='ipv4'",
    "uci commit",
    "reboot"
    ]
    start_cfg_3G = cfg_wwan_BM10("root", "192.168.1.1", "root", cfg_commands)
    print(start_cfg_3G)
    time.sleep(30)
if __name__ == "__main__":
    print(ping_ip("192.168.1.1","8.8.8.8", "root", "root"))

