#!/usr/bin/python3

"""
rac: 2022-03-21 fix-zerotier-mtu.py
This program tries to set a better mtu for the zerotier interface
"""

import sys
import subprocess

DEFAULT_MTU='2800'

# check that we were given at least on argument
# 0=program name, 1=ip_address
if len(sys.argv) < 2:
    print ('usage:')
    print ('      ', sys.argv[0], ' ip.add.re.ss')
    sys.exit(1)
ip_dst = sys.argv[1]



# use 'ip route get' to find the interface used in the route to this ip
ip_route_get = "ip route get %s | grep -Po '(?<= dev ).+?(?= (src|proto))'" %ip_dst
interface = subprocess.getoutput(ip_route_get)


# ensure we only change the MTU on a zerotier interface (starts with 'zt')
if not interface.lower().startswith('zt'):
    print ('ERROR: the interface %s does not appear to be a zerotier interface.' %interface)
    sys.exit(1)


# (re)set the mtu to zt default_mtu
print ('setting the mtu on interface %s to %s' %(interface, DEFAULT_MTU))
ip_link_set = 'ip link set %s mtu %s' %(interface, DEFAULT_MTU)
subprocess.getoutput(ip_link_set)


# find the optimal MTU using ping -M do
print ('please wait, checking for optimal MTU to %s via %s' %(ip_dst, interface))
cmd="""bash -c "for i in {900..1500..2}; do ping -M do -c 1 %s -s \$i 2>&1 | grep -q '0 received' && break; done; echo \$((\$i - 2));" """ %ip_dst
mtu=subprocess.getoutput(cmd)


# time to actually set the MTU
print ('setting the mtu on interface %s to %s' %(interface, mtu))
ip_link_set = 'ip link set %s mtu %s' %(interface, mtu)
subprocess.getoutput(ip_link_set)
