

import re
import pexpect
from pprint import pprint

def send_show_ifcof(ip, user, password, commands):#f-show all ifconf
    print(f"Connect to {ip}")
    output=()
    try:
        with pexpect.spawn(f"ssh {user}@{ip}", timeout=10, encoding="utf-8") as ssh:
            ssh.expect("d:")
            ssh.sendline(password)
            ssh.expect("root@BWOS:~#")
            if type(commands)== str:
                commands=[commands]
            for cmd in commands:
                ssh.sendline(cmd)
                ssh.expect("root@BWOS:~#")
                temp = ssh.before
                if "addr:" in temp:
                    output = re.search(r'addr:(\S+)', temp).group()
                else:
                    print("no int")
        return output
    except pexpect.exceptions.TIMEOUT as error:
        print(f"error connect to {ip}")

if __name__=="__main__":
    pprint(send_show_ifcof("192.168.2.1", "root", "128500", ["ifconfig | grep -A 2  wlan0",]),width=120)
