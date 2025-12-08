---
description: Configuració del servei DHCP a Ubuntu Server 24.04
---

# ⚒ Configuració del servei DHCP a Ubuntu 24.04

Partim d'una màquina virtual, amb un sistema operatiu basat a Ubuntu Server 24.04, i que té configurades dues interfícies de xarxa:

* Una connectada a NAT, perquè el servidor tinga accés a internet i puga instal·lar paquets.

<figure><img src=".gitbook/assets/image (3).png" alt=""><figcaption><p>Configuració de la interfície de xarxa de VirtualBox a NAT</p></figcaption></figure>

* Una connectada a la xarxa interna 'aula'.

<figure><img src=".gitbook/assets/image (1).png" alt=""><figcaption><p>Configuració de la interfície de xarxa de VirtualBox a Xarxa interna 'aula'</p></figcaption></figure>

Obrim un terminal, per a fer les operacions de configuració:

* [ ] Instal·lem el servei DHCP a ubuntu

```bash
profe@sx-srv-profe-dhcp:~$ sudo apt install isc-dhcp-server
[sudo] password for profe:
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following additional packages will be installed:
  libirs-export161 libisccfg-export163
Suggested packages:
  isc-dhcp-server-ldap policycoreutils
The following NEW packages will be installed:
  isc-dhcp-server libirs-export161 libisccfg-export163
0 upgraded, 3 newly installed, 0 to remove and 0 not upgraded.
Need to get 529 kB of archives.
After this operation, 1546 kB of additional disk space will be used.
Do you want to continue? [Y/n]
```

* [ ] Editem el fitxer de configuració del servei, localitzar a la ruta **/etc/dhcp/dhcpd.conf** amb el nostre editor de text preferit, i **amb permisos d'administrador** (fent servir sudo, si cal):

```bash
profe@sx-srv-profe-dhcp:~$ sudo vi /etc/dhcp/dhcpd.conf
```

Al fitxer, respectant el format, haurem d'incloure els paràmetres de configuració del servei DHCP. Per a l'exemple, configurarem els següents paràmetres de xarxa:

* Temps per defecte d'expiració de les IP: 600 segons
* Temps màxim d'expiració de les IP: 700 segons
* xarxa 192.168.0.0/24
* Porta d'enllaç 192.168.0.1&#x20;
* rang d'IP disponibles 192.168.0.100 - 192.168.0.200&#x20;
* DNS per defecte: 8.8.8.8 i 8.8.4.4.&#x20;

```editorconfig
default-lease-time 600;
max-lease-time 7200;

subnet 192.168.0.0 netmask 255.255.255.0 {
 range 192.168.0.150 192.168.0.175;
 option routers 192.168.0.1;
 option domain-name-servers 8.8.8.8, 8.8.4.4;
 option domain-name "aula.local";
}
```

A continuació, editarem el fitxer de configuració **/etc/default/isc-dhcp-server** per a indicar les targetes de xarxa que acceptaran peticions DHCP.

```bash
profe@sx-srv-profe-dhcp:~$ sudo vi /etc/default/isc-dhcp-server
```

Al nostre cas, la targeta de xarxa que es troba a la xarxa interna aula és l'enp0s8, per tant, haurem d'indicar-lo així al fitxer:

```
# On what interfaces should the DHCP server (dhcpd) serve DHCP requests?
#       Separate multiple interfaces with spaces, e.g. "eth0 eth1".
INTERFACESv4="enp0s8"
INTERFACESv6=""
```

* [ ] Apliquem la configuració:

Perquè el nostre servei DHCP comence a funcionar, hem d'iniciar el servei, executant els següents comandaments:

```bash
profe@sx-cli-profe01:~$ sudo systemctl enable isc-dhcp-server.service
profe@sx-cli-profe01:~$ sudo systemctl start isc-dhcp-server.service
profe@sx-cli-profe01:~$ sudo systemctl status isc-dhcp-server.service
```

En el cas que vulguem reiniciar el servei, perquè hem canviat la configuració, podrem parar i arrancar el servei, o reiniciar-lo:&#x20;

```bash
profe@sx-cli-profe01:~$ sudo service isc-dhcp-server.service stop;
profe@sx-cli-profe01:~$ sudo service isc-dhcp-server.service start;
```

O reiniciar-lo

```bash
profe@sx-cli-profe01:~$ sudo service isc-dhcp-server.service restart;
```

i posteriorment, podem comprovar l'estat del servei:

```bash
profe@sx-cli-profe01:~$ sudo service isc-dhcp-server.service status;
```

En el cas que el servei no arranque de manera correcta, podem mirar els fitxers de log del sistema, per trobar alguna pista que ens ajude a solucionar l'error.&#x20;

```bash
profe@sx-cli-profe01:~$ cat /var/log/syslog;
```

* [ ] Comprovem que el servei funciona correctament:

Per a provar que tot funciona correctament, podem configurar una nova màquina virtual a la nostra xarxa interna, indicant en la seva configuració de xarxa que ha de demanar els paràmetres de la configuració de xarxa al servei DHCP:

```bash
profe@sx-cli-profe02:~$ cat /etc/netplan/01-network-manager-all.yaml 
# Let NetworkManager manage all devices on this system
network:
  version: 2
# ⚠️ **ATENCIÓ:**
# Si estàs utilitzant **Ubuntu Server** en comptes de Desktop, probablement hauries de posar `renderer: networkd` en lloc de `NetworkManager`.
# Ubuntu Desktop utilitza NetworkManager per defecte, però Ubuntu Server NO.
# Si utilitzes `renderer: NetworkManager` en Server, i NetworkManager NO està instal·lat i habilitat, la xarxa NO funcionarà.
# Pots canviar el valor del renderer ací segons el teu cas.


  renderer: NetworkManager
  ethernets:
    enp0s3:
      dhcp4: true
```

* Podem aplicar la configuració de la xarxa, i comprovar els paràmetres assignats:

```bash
profe@sx-cli-profe02:~$ sudo netplan apply

profe@sx-cli-profe02:~$ ifconfig
enp0s3: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.0.150  netmask 255.255.255.0  broadcast 192.168.0.255
        inet6 fe80::a00:27ff:fe30:345c  prefixlen 64  scopeid 0x20<link>
        ether 08:00:27:30:34:5c  txqueuelen 1000  (Ethernet)
        RX packets 9  bytes 1670 (1.6 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 255  bytes 28864 (28.8 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Bucle local)
        RX packets 94  bytes 9484 (9.4 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 94  bytes 9484 (9.4 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

profe@sx-cli-profe02:~$ ip route show
default via 192.168.0.1 dev enp0s3 proto dhcp metric 100 
192.168.0.0/24 dev enp0s3 proto kernel scope link src 192.168.0.150 metric 100 

profe@sx-cli-profe02:~$ nmcli dev show enp0s3 | grep IP4
IP4.ADDRESS[1]:                         192.168.0.150/24
IP4.GATEWAY:                            192.168.0.1
IP4.ROUTE[1]:                           dst = 192.168.0.0/24, nh = 0.0.0.0, mt = 100
IP4.ROUTE[2]:                           dst = 0.0.0.0/0, nh = 192.168.0.1, mt = 100
IP4.DNS[1]:                             8.8.8.8
IP4.DNS[2]:                             8.8.4.4
IP4.DOMAIN[1]:                          aula.local

profe@sx-srv-profe-dhcp:~$ sudo networkctl status
●        State: routable
  Online state: online
       Address: 192.168.0.150 on enp0s3
                fe80::a00:27ff:fee5:1603 on enp0s3
       Gateway: 192.168.0.1 on enp0s3
           DNS: 8.8.8.8
                8.8.4.4
```

Si volem comprovar la informació sobre les IP concedides pel servidor, podem visualitzar el contingut del fitxer del servidor **/var/lib/dhcp/dhcp.leases**&#x20;

```bash
profe@sx-srv-profe-dhcp:~$ cat /var/lib/dhcp/dhcpd.leases
# The format of this file is documented in the dhcpd.leases(5) manual page.
# This lease file was written by isc-dhcp-4.4.1

# authoring-byte-order entry is generated, DO NOT DELETE
authoring-byte-order little-endian;

lease 192.168.0.150 {
  starts 3 2023/09/27 11:31:34;
  ends 3 2023/09/27 11:41:34;
  tstp 3 2023/09/27 11:41:34;
  cltt 3 2023/09/27 11:31:34;
  binding state free;
  hardware ethernet 08:00:27:30:34:5c;
  uid "\001\010\000'04\\";
}
server-duid "\000\001\000\001,\246\314\260\010\000'\255i%";

lease 192.168.0.151 {
  starts 4 2023/09/28 15:05:39;
  ends 4 2023/09/28 15:15:39;
  cltt 4 2023/09/28 15:05:39;
  binding state active;
  next binding state free;
  rewind binding state free;
  hardware ethernet 08:00:27:71:fe:bd;
  uid "\001\010\000'q\376\275";
  client-hostname "sx-cli-jorge-02";
}
```

