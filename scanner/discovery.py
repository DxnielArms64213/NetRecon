import subprocess
import ipaddress
from typing import Iterable

def ping_host(ip:ipaddress.IPv4Address|ipaddress.IPv6Address)->bool:
    """ ping_host() receives one IP address produced by expand_target(), attempts to ping it, and returns True or False based on the result."""
    if isinstance(ip, (ipaddress.IPv4Address)):
        ping_version="-4"
    else:
        ping_version="-6"
    result=subprocess.run(["ping", ping_version, "-n", "1", "-w", "1000", str(ip)], capture_output=True)
    return result.returncode == 0

def discover_hosts(targets:Iterable[ipaddress.IPv4Address|ipaddress.IPv6Address])->list[ipaddress.IPv6Address|ipaddress.IPv4Address]:
    """creates a list then pings every ip in target if the ping is succesful it is appended to the list and returned"""
    alive_hosts=[]
    for ip in targets:
        ping=ping_host(ip)
        if ping:
            alive_hosts.append(ip)
    return alive_hosts


            