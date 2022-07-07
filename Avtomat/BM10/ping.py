import re
import pexpect

def ping_ip_3G (ip_s, ip_dest, user, password):
    result=""
    with pexpect.spawn(f"ssh {user}@{ip_s}", timeout=10, encoding="utf-8") as ssh:
        ssh.expect("d:")
        ssh.sendline(password)
        ssh.expect("root@BWOS:~#")

        ssh.send("ping ")
        ssh.send(ip_dest)
        ssh.sendline(" -w 5")
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

if __name__ == "__main__":
    print(ping_ip_3G("192.168.1.1","8.8.8.8", "root", "root"))
