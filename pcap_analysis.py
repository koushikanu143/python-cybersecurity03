import pyshark

def analyze_pcap(file):
    print(f"\n[+] Analyzing {file}")

    cap = pyshark.FileCapture(file, tshark_path=r"C:\Program Files\Wireshark\tshark.exe")

    dns_count = 0
    arp_count = 0
    sqli_flag = False

    for packet in cap:
        try:
            if 'DNS' in packet:
                dns_count += 1

            if 'ARP' in packet:
                arp_count += 1

            if 'HTTP' in packet:
                if "UNION" in str(packet.http) or "OR 1=1" in str(packet.http):
                    sqli_flag = True

        except:
            continue

    print("DNS Packets:", dns_count)
    print("ARP Packets:", arp_count)

    if dns_count > 100:
        print("⚠ Possible DNS Tunneling")

    if arp_count > 50:
        print("⚠ Possible ARP Spoofing")

    if sqli_flag:
        print("⚠ SQL Injection Attempt Detected")

pcap_files = [
    "dns_tunnel.pcap",
    "sqli.pcap",
    "arp_spoof.pcap"
]

for file in pcap_files:
    analyze_pcap(file)