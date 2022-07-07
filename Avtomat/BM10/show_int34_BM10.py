
import sys
import re
import pexpect
from pprint import pprint

def send_show_ifcof(ip, user, password, log = True):#f-show all ifconf
    if log:
        print(f"Connect to {ip}...")
    result=''
    try:
        with pexpect.spawn(f"ssh {user}@{ip}", timeout=10, encoding="utf-8") as ssh:
            ssh.expect("d:")
            ssh.sendline(password)
            ssh.expect("root@BWOS:~#")
            print(ip, "connected")

            ssh.sendline("uci show network | grep 34G")
            ssh.expect("root@BWOS:~#")
            temp = ssh.before
            for sec in temp:
                if "34G.device" in temp:
                    name_intf = re.search(r'network.(\S+).device', temp).group()
                    result += name_intf

                    ssh.sendline("ifconfig |grep -A 1 wwan0")
                    ssh.expect("root@BWOS:~#")
                    temp = ssh.before

                    if "addr:" in temp:
                        ip_int = re.search(r'inet addr:(\S+)', temp).group()
                        result += ip_int
                    else:
                        result = name_intf
                        print("*"*30)
                        print(name_intf," exist, but d'nt have ip addr")
                    break
                else:
                    result="No interface on router"
                    break
        return result
    except pexpect.exceptions.TIMEOUT as error:
        print(f"Error connect to {ip}")

if __name__=="__main__":
    print(send_show_ifcof("192.168.2.1", "root", ""))

