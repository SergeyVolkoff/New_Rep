import paramiko
from scp import SCPClient

def pppoe(server, port, user, password):
        client = paramiko.SSHClient()
        #client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port, user, password)
        return client
host = '192.168.1.1'
user = 'root'
password = 'root'
port = 22
ssh = pppoe(host, port, user, password)
scp = SCPClient(ssh.get_transport())

PPP=scp.put('/home/ssw/new/New_Rep/Avtomat/BM10/pppoe_cfg_file/pppoe', '/etc/config/')
print(PPP)
P_serv=scp.put('/home/ssw/new/New_Rep/Avtomat/BM10/pppoe_cfg_file/pppoe-server-options', '/etc/ppp/')
print(P_serv)
scp.put('/home/ssw/new/New_Rep/Avtomat/BM10/pppoe_cfg_file/chap-secrets', '/etc/ppp/')
scp.close()
ssh.close()

if __name__ == "__main__":
        host = '192.168.1.1'
        user = 'root'
        password = 'root'
        port = 22
        print(pppoe(host,user,password))