import subprocess
from concurrent.futures import ThreadPoolExecutor


def ping_ip(ip):
    result = subprocess.run(["ping", "-c", "10", "-n", ip], stdout=subprocess.DEVNULL)
    ip_is_reachable = result.returncode == 0
    return ip_is_reachable


def ping_ip_addresses(ip_list, limit=20):
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
    print(ping_ip_addresses([
        "193.104.189.68",
        "188.165.255.116",
        "46.101.114.69",
        "188.68.231.113",
        "85.14.243.31",
        "185.152.64.53",
        "80.91.125.238",
        "207.246.103.49",
        "190.109.17.218",
        "41.128.148.86",
        "181.12.111.26",
        "101.109.13.229",
        "103.252.1.137",
        "182.53.110.17",
        "185.169.183.173",
        "14.241.80.150",
        "189.91.150.205",
        "159.65.133.175",
        "210.212.227.67",
        "105.213.177.51",
        "164.68.117.160",
        "190.60.37.51",
        "103.154.146.66",
        "87.202.23.199",
        "194.233.95.214",
        "177.43.213.80",
        "31.171.152.69",
        "118.136.85.170",
        "154.236.189.25",
        "36.79.194.93",
        "91.144.158.238",
        "88.255.217.40",
        "101.109.21.195",
        "190.131.195.2",
        "36.85.115.132",
        "154.212.7.248",
        "45.167.126.249",
        "102.69.234.190",
        "45.225.106.100",
        "201.182.87.1",
        "191.110.89.158",
        "105.213.118.7",
        "27.54.117.162",
        "180.243.198.110",
        "131.255.100.12",
        "182.253.247.241",
        "101.109.8.23",
        "45.71.196.193",
        "103.244.38.36",
        "81.162.67.76"
    ]))