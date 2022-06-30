
import re
import pexpect
from pprint import pprint
from show_BM10 import send_show_ifcof




def cfg_wwan_BM10(user,ip, password,cfg_commands):
    output = ""
    for cmd in cfg_commands:
        with pexpect.spawn(f"ssh {user}@{ip}", timeout=10, encoding="utf-8") as ssh:
            ssh.expect("d:")
            ssh.sendline(password)
            ssh.expect("root@BWOS:~#")
            cfg_commands = [*cfg_commands]
            ssh.sendline(cmd)
            ssh.expect("root@BWOS:~#")
            ssh.sendline("uci show network | grep 34G")
            temp = ssh.before
            if "34G.pdptype" in temp:
                pprint("3G int greate in process")
            ssh.sendline("reboot")




if __name__ == "__main__":
    cfg_commands = [
    "uci set network.34G=interface",
    "uci set network.34G.proto='qmi'",
    "uci set network.34G.device='/dev/cdc-wdm0'",
    "uci set network.34G.apn='internet.tele2.ru'",
    "uci set network.34G.pdptype='ipv4'",
    "uci commit",
    "reboot"
    ]

    output= cfg_wwan_BM10("root", "192.168.1.1", "root", cfg_commands)


