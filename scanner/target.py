
import ipaddress   
from typing import Iterator 

#Gets target input then validates it by attempting to turn it into a IP address IP network or an IP range
def get_target():
    while True:
        raw_target=input("Enter target: ").strip()
        try:
            target=ipaddress.ip_address(raw_target)
            return target
        except ValueError:
            try:
                target=ipaddress.ip_network(raw_target, strict=False)
                return target
            except ValueError:
                try:
                    target_range=parse_target(raw_target)
                    return target_range
                except ValueError:
                    print("Invalid Target: Enter an IP address, CIDR network, or IP range")
                  

def expand_target(target)-> Iterator[ipaddress.IPv4Address | ipaddress.IPv6Address]:
    """Expands a validated target into individual IP addresses for scanning."""
    if isinstance(target, (ipaddress.IPv4Address, ipaddress.IPv6Address)):
        yield target
    elif isinstance(target, (ipaddress.IPv4Network, ipaddress.IPv6Network)):
        for ip in target.hosts():
            yield ip
    elif hasattr(target, "__iter__"):
        for ip in target:
            yield ip
    else:
         raise ValueError("unsupported target type")


def parse_target(target: str)->Iterator[ipaddress.IPv4Address | ipaddress.IPv6Address]:
    """Parses an IP range and generates each address within the specified range."""
    if "-" not in target:
        raise ValueError()
    parts=target.split("-")
    if len(parts)!=2:
        raise ValueError()
    start=parts[0].strip()
    end=parts[1].strip()
    start=ipaddress.ip_address(start)
    end=ipaddress.ip_address(end)
    if start.version != end.version:
        raise ValueError()
    if start>end:
        raise ValueError()
    return (ipaddress.ip_address(ip) for ip in range(int(start), int(end) + 1))

print(list(expand_target(get_target())))