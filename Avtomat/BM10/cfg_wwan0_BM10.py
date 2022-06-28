
import re
import pexpect
from pprint import pprint
from show_BM10 import send_show_ifcof




def cfg_wwan_BM10(user,ip, password,cfg_commands):
    output = send_show_ifcof("192.168.2.1", "root", "128500", ["uci show network | grep 34G"])
    for cmd in cfg_commands:
        if "34G" in output:
            pprint(" int already exists")
        else:
            with pexpect.spawn(f"ssh {user}@{ip}", timeout=10, encoding="utf-8") as ssh:
                ssh.expect("d:")
                ssh.sendline(password)
                ssh.expect("root@BWOS:~#")
                cfg_commands = [*cfg_commands]
                ssh.sendline(cmd)
                ssh.expect("root@BWOS:~#")
                ssh.sendline("uci show network | grep 34G")
                temp = ssh.before
                print(temp)
                if "ip" in output:
                    pprint(" int greate")


if __name__ == "__main__":
    cfg_commands = [
    "uci set network.34G=interface",
    "uci set network.34G.proto='qmi'",
    "uci set network.34G.apn='internet.tele2.ru'",
    "uci set network.34G.pdptype='ipv4'",
    "uci commit"
    ]
    out = cfg_wwan_BM10("root", "192.168.2.1", "128500", cfg_commands)
    print(out)

