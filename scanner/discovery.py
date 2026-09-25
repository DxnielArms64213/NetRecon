import subprocess

def ping_host(ip):
    result=subprocess.run(["ping","-n", "1", "-w", 1000, str(ip)])
    if result.returncode==0:
        ping=True
        return ping
    else:
        ping=False
        return ping

def discover_hosts(targets):
    alive_hosts=[]
    for ip in targets:
        ping=ping_host(ip)
        if ping:
            alive_hosts.append(ip)
    return alive_hosts


            