# zerotier-fix-mtu
A Linux script to set the MTU on Zerotier interfaces (when given a known endpoint IP/domain)


A better approach is probably to simply set tcp_mtu_probing on your system, but this will affect all interfaces, thus is not as targeted:

`echo 1 >/proc/sys/net/ipv4/tcp_mtu_probing`


I will add more here as I find time, this is just the start.
