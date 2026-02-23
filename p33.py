from scapy.all import sniff

def show(packet):
    print(packet.summary())

sniff(count=10, prn=show)