import ipaddress
import subprocess as sp


def get_nic_ipv4(nic):
    """
        Get IP address from a NIC.

        Parameter
        ---------
        nic : str
            Network Interface Card used for the query.

        Returns
        -------
        ipaddr : str
            Ipaddress from the NIC provided as parameter.
    """
    try:
        result = sp.check_output(["ip", "-4", "addr", "show", nic],
                                 stderr=sp.STDOUT)
    except Exception:
        return "Unkown NIC: %s" % nic
    result = result.decode().splitlines()
    print(result)
    ipaddr = [l.split()[1] for l in result if "inet" in l]
    return ipaddr[0]


print(get_nic_ipv4("enp0s31f6"))


def get_nics():
    """
        Get all NICs from the Operating System.

        Returns
        -------
        nics : list
            All Network Interface Cards.
    """
    result = sp.check_output(["ip", "addr", "show"])
    result = result.decode().splitlines()
    nics = [l.split()[1].strip(':') for l in result if l[0].isdigit()]
    return nics

print(get_nics())


interface = ipaddress.IPv4Interface("{}/{}".format("192.168.15.10", 24))
print(interface)
vendor_name