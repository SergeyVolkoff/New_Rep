import subprocess
from concurrent.futures import ThreadPoolExecutor


def ping_ip(ip):
    result = subprocess.run(["ping", "-c", "1000", "-n", ip], stdout=subprocess.DEVNULL)
    ip_is_reachable = result.returncode == 0
    return ip_is_reachable


def ping_ip_addresses(ip_list, limit=250):
    reachable = []
    unreachable = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        results = executor.map(ping_ip, ip_list)
    for ip, status in zip(ip_list, results):
        if status:
            reachable.append(ip)
        else:
            unreachable.append(ip)
    return reachable, unreachable


if __name__ == "__main__":
    a=1
    ip = []
    while a<1000:
        ip.append("192.168.2.1")
        a += 1
    print(ip)
    print(ping_ip_addresses(ip))



