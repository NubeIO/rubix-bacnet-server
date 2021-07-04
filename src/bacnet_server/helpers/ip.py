import ipaddress
import subprocess as sp


class IP:

    @staticmethod
    def format_ip_mask(ip: str, port: int):
        return ipaddress.IPv4Interface("{}/{}".format(ip, port))

    @staticmethod
    def get_nic_ipv4(nic: str):
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
            return False
        result = result.decode().splitlines()
        ipaddr = [l.split()[1] for l in result if "inet" in l]
        return ipaddr[0]

    @staticmethod
    def get_nic_list() -> []:
        """
            Get all NICs from the Operating System.

            Returns
            -------
            nics : list
                All Network Interface Cards.
        """
        result = sp.check_output(["ip", "addr", "show"])
        result = result.decode().splitlines()
        n = [l.split()[1].strip(':') for l in result if l[0].isdigit()]
        return n



