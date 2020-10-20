#-*- coding: utf-8 -*- #
# !/usr/bin/python

from base import *
from scapy.all import *

def capture_diam(pkt):
	ip = pkt.getlayer(IP)
	sctp = pkt.getlayer(SCTP)
	last = pkt.lastlayer()

	if last.type == 0:
		cmd = DiaMessage()
		cmd.decode(last.data)
		print('[ src ip/port = ', ip.src, sctp.sport, 'dst ip/port = ', ip.dst, sctp.dport, ' ]')
		ip.show()
		#sctp.show()
		display_cmd(cmd)
		hexdump(ip)
		print('')
	else:
		print('[ src ip/port = ', ip.src, sctp.sport, 'dst ip/port = ', ip.dst, sctp.dport, ' ]')
		hexdump(ip)
		print('')

sniff(iface="lo", filter="port 3868", store=0, prn=capture_diam)
