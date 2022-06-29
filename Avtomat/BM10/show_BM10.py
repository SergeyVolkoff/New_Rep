
import sys
import re
import pexpect
from pprint import pprint

def send_show_ifcof(ip, user, password):#f-show all ifconf
    print(f"Connect to {ip}...")
    output=()
    try:
        with pexpect.spawn(f"ssh {user}@{ip}", timeout=10, encoding="utf-8") as ssh:
            ssh.expect("d:")
            ssh.sendline(password)
            ssh.expect("root@BWOS:~#")
            print(ip, "connected")

            ssh.sendline("uci show network | grep 34G")
            ssh.expect("root@BWOS:~#")
            temp = ssh.before
            if "34G.device" in temp:
                name_intf = re.search(r'network.(\S+).device', temp).group()
                return name_intf

            else:
                print('_'*30, "\nNo interface on router, \nfor greate - input cfg_wwan_BM10")
                return

            ssh.sendline("ifconfig |grep -A 1 wwan0")
            ssh.expect("root@BWOS:~#")
            temp = ssh.before

            if "addr:" in temp:
                ip_int = re.search(r'inet addr:(\S+)', temp).group()
                print(name_intf,"exist with", ip_int)
                return ip_int
            else:
                print('_'*30, "\n No ip on int, \nbut int greate - maibee reboot?")


    except pexpect.exceptions.TIMEOUT as error:
        print(f"Error connect to {ip}")

if __name__=="__main__":
    pprint(send_show_ifcof("192.168.1.1", "root", "root"))

