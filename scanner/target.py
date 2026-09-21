
import ipaddress    


def get_target():
    valid_target=False
    while valid_target==False:
        target=input("Enter target: ").strip()
        try:
            target=ipaddress.ip_address(target)
            valid_target=True
            return target
        except ValueError:
            try:
                target=ipaddress.ip_network(target)
                valid_target=True
                return target
            except ValueError:
                try:
                    target_range=parse_target(target)
                    return target_range
                except ValueError:
                    print("enter a valid target")
                  

def expand_target(target):
    if isinstance(target, (ipaddress.IPv4Address, ipaddress.IPv6Address)):
        return [target]
    elif isinstance(target, (ipaddress.IPv4Network, ipaddress.IPv6Network)):
        return list(target)
    elif isinstance(target, list):
        return target
    else:
         raise ValueError
ipaddress.i

def parse_target(target):
    if "-" not in target:
        raise ValueError()
    parts=target.split("-")
    ips=[]
    start=parts[0].strip()
    end=parts[1].strip()
    start=ipaddress.ip_address(start)
    end=ipaddress.ip_address(end)
    if len(parts)!=2:
        raise ValueError
    if start.version != end.version:
        raise ValueError
    if start>end:
        raise ValueError
    for ip in range(int(start), int(end)+1):
        current_ip=ipaddress.ip_address(ip)
        ips.append(current_ip)
    return ips

get_target()