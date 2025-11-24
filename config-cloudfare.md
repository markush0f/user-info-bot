sudo nano /etc/resolv.conf

nameserver 1.1.1.1
nameserver 1.0.0.1

sudo systemctl restart systemd-resolved

sudo nano /etc/sysctl.conf

net.ipv6.conf.all.disable_ipv6 = 0
net.ipv6.conf.default.disable_ipv6 = 0

sudo sysctl -p

ping6 db.epqzqwovleotajepkpcw.supabase.co
