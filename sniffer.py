#!/usr/bin/env python3
"""Simple packet sniffer built with Scapy.

Prints timestamp, source IP, destination IP, protocol, and ports for each packet.
Run with: sudo python3 sniffer.py [-i INTERFACE] [-f BPF_FILTER]
Only sniff networks you own or have permission to monitor.
"""
import argparse
from datetime import datetime
from scapy.all import sniff, IP, IPv6, TCP, UDP, ICMP, ARP, DNS, DNSQR

def handle(pkt):
    ts = datetime.now().strftime("%H:%M:%S")

    if pkt.haslayer(IP):
        src, dst = pkt[IP].src, pkt[IP].dst
    elif pkt.haslayer(IPv6):
        src, dst = pkt[IPv6].src, pkt[IPv6].dst
    elif pkt.haslayer(ARP):
        print(f"[{ts}] ARP   {pkt[ARP].psrc} -> {pkt[ARP].pdst}")
        return
    else:
        return

    if pkt.haslayer(DNS) and pkt.haslayer(DNSQR):
        proto = f"DNS   (query: {pkt[DNSQR].qname.decode(errors='ignore')})"
    elif pkt.haslayer(TCP):
        proto = f"TCP   {pkt[TCP].sport} -> {pkt[TCP].dport}"
    elif pkt.haslayer(UDP):
        proto = f"UDP   {pkt[UDP].sport} -> {pkt[UDP].dport}"
    elif pkt.haslayer(ICMP):
        proto = "ICMP"
    else:
        proto = "OTHER"

    print(f"[{ts}] {src:<15} -> {dst:<15} | {proto}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Tiny Scapy packet sniffer")
    p.add_argument("-i", "--iface", help="interface (e.g. eth0, wlan0)")
    p.add_argument("-f", "--filter", default="", help="BPF filter (e.g. 'icmp')")
    args = p.parse_args()

    print("Sniffing... press Ctrl+C to stop\n")
    sniff(iface=args.iface, filter=args.filter, prn=handle, store=False)