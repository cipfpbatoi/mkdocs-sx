---
description: Configuració d'una porta d'enllaç amb Ubuntu server 24.04 i el programari ufw
---

# ⚒ Configuració del servei de routing a Ubuntu Server 24.04

### Escenari inicial:

En aquest exemple, partim d'una configuració de xarxa com la mostrada a la següent imatge:

<figure><img src="../.gitbook/assets/UD00P01. esquema de red a configurar.png" alt=""><figcaption></figcaption></figure>

Suposem configurades les targetes de xarxa interna de les màquines virtuals, amb IP fixa, dins de la xarxa 192.168.0.0/24.

Les màquines clients disposaran d'una IP a partir de la 192.168.0.101.

La màquina server, configurada amb un sistema operatiu basat a Ubuntu Server 24.04, disposarà de dues targetes de xarxa:

* La primera configurada a la xarxa aula, amb la IP fixa 192.168.0.100. Aquesta interfície de xarxa treballarà com a porta d'enllaç per a connectar a internet a les màquines de la xarxa aula que ho necessiten.&#x20;
* La segona configurada com a xarxa NAT o Bridge, i assignació d'IP amb protocol DCHP.

Totes les màquines de la xarxa aula poden comunicar-se internament (podem executar un ping i funciona correctament).

### Comprovació de la connectivitat entre les màquines:

Comprovem que la màquina sx-srv-xxxx01 pot connectar a internet:

```bash
profe@sx-srv-profe01:~$ wget www.google.com
--2023-09-23 10:55:56--  http://www.google.com/
Resolving www.google.com (www.google.com)... 142.250.184.164, 2a00:1450:4003:80c::2004
Connecting to www.google.com (www.google.com)|142.250.184.164|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: unspecified [text/html]
Saving to: ‘index.html’

index.html                                          [ <=>                                                                                                 ]  23.51K  --.-KB/s    in 0.008s  

2023-09-23 10:55:56 (2.76 MB/s) - ‘index.html’ saved [24073]

```

També comprovem que tenim connectivitat entre les màquines sx-srv-xxxx01 i sx-cli-xxxx01

```bash
/profe@sx-srv-profe01:~$ ping sx-cli-profe01
PING sx-cli-profe01 (192.168.0.101) 56(84) bytes of data.
64 bytes from sx-cli-profe01 (192.168.0.101): icmp_seq=1 ttl=64 time=0.812 ms
64 bytes from sx-cli-profe01 (192.168.0.101): icmp_seq=2 ttl=64 time=1.10 ms
64 bytes from sx-cli-profe01 (192.168.0.101): icmp_seq=3 ttl=64 time=0.368 ms
```

### Habilitar les funcionalitats de routing i NAT en la màquina sx-srv-xxxx-01:

* [ ] Instal·lem el programari ufw (uncomplicated firewall), habilitem les connexions SSH i activem el servei instal·lat.

```bash
sudo apt install ufw;
sudo ufw allow OpenSSH;
sudo ufw enable;
```

* [ ] Editem el fitxer de configuració **/etc/ufw/sysctl.conf**, per activar les funcionalitats de routing del servei ufw, modificant o afegint l'entrada **net/ipv4/ip\_forward** amb valor **1.**

<pre class="language-systemd"><code class="lang-systemd"><strong># Uncomment this to allow this host to route packets between interfaces
</strong>net/ipv4/ip_forward=1
</code></pre>

* [ ] Editem el fitxer de configuració **/etc/default/ufw** per a habilitar les funcionalitats de NAT al server, assignant a l'entrada **DEFAULT\_FORWARD\_POLICY** el valor **ACCEPT** &#x20;

```systemd
# Set the default forward policy to ACCEPT, DROP or REJECT.  Please note that
# if you change this you will most likely want to adjust your rules
DEFAULT_FORWARD_POLICY="ACCEPT"
```

* [ ] Editem el fitxer de configuració **/etc/ufw/before.rules** per a afegir, a l'inici del fitxer, les regles d'encaminament a aplicar pel sistema, respectant el format indicat.

```systemd
#NAT
*nat
:POSTROUTING ACCEPT [0:0]
-A POSTROUTING -s 192.168.0.1/24 -o enp0s3 -j MASQUERADE
COMMIT

```

La configuració introduïda:

* Habilita les funcionalitats de nat.
* Configura la **redirecció** del tràfic de xarxa provinent **de la xarxa 192.168.0.1/24** per la targeta de xarxa **enp0s3**, configurada anteriorment com xarxa NAT amb DCHP.
* Configurat l'emmascarament de la IP d'origen de les peticions redirigides.

<!---->

* [ ] Reiniciem el servei ufw, amb la nova configuració, i comprovem que continuem tenint connexió a internet, i amb la xarxa interna des del servidor:

```bash
sudo ufw disable;
sudo ufw enable;
sudo ufw status;
```

Comprovem que la màquina sx-srv-xxxx01 té connexió amb qualsevol servidor DNS d'internet:

```bash
profe@sx-srv-profe01:~$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=119 time=21.7 ms
```

Comprovem que continuem tenim connectivitat amb una màquina de la xarxa aula:

```bash
profe@sx-srv-profe01:~$ ping sx-cli-profe01
PING sx-cli-profe01 (192.168.0.101) 56(84) bytes of data.
64 bytes from sx-cli-profe01 (192.168.0.101): icmp_seq=1 ttl=64 time=0.646 ms
```

### Configuració de la porta d'enllaç a la màquina client

Per començar, comprovarem que la màquina client encara no té connectivitat amb internet, fent un ping des de sx-cli-xxxx01 a un servidor DNS d'internet:

```bash
profe@sx-cli-profe01:~$ ping 8.8.8.8
ping: connect: La red es inaccesible
```

És així perquè encara no hem configurat la porta d'enllaç en la configuració de xarxa de la màquina client:

```bash
profe@sx-cli-profe01:~$ networkctl status
●        State: routable                          
  Online state: unknown
       Address: 192.168.0.101 on enp0s3
                fe80::a00:27ff:fedf:63c6 on enp0s3

```

{% hint style="warning" %}
En cas de que aparega l'advertencia **"WARNING: systemd-networkd is not running, output will be incomplete."**, haurem de iniciar el servei **systemd-networkd** amb els següents commandaments:

<pre><code><strong>$ sudo systemctl start systemd-networkd;
</strong><strong>$ sudo systemctlenable systemd-networkd;
</strong></code></pre>
{% endhint %}

Afegim la porta d'enllaç editant el fitxer de configuració Yaml de netplan, a la ruta /etc/netplan/ i editant o afegint la propietat **routes** amb els paràmetres **to** (xarxa desti) i **via** (IP de la porta d'enllaç a utilitzar per accedir a la xarxa destí). Al nostre cas particular, indicarem que la porta d'enllaç per defecte és el server configurat amb la IP 192.168.0.100.

```bash
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
      addresses:
      - 192.168.0.101/24
      routes:
        - to: default
          via: 192.168.0.100
      dhcp4: false

```

Guardem el fitxer de configuració i apliquem els canvis al sistema:

```
profe@sx-cli-profe01:~$ sudo netplan apply;
```

Comprovem que la configuració de la porta d'enllaç està correctament configurada al sistema:

```bash
profe@sx-cli-profe01:~$ networkctl status
●        State: routable                          
  Online state: unknown
       Address: 192.168.0.101 on enp0s3
                fe80::a00:27ff:fedf:63c6 on enp0s3
       Gateway: 192.168.0.100 on enp0s3
```

I provem si la màquina client té connectivitat amb internet, fent un ping des de sx-cli-xxxx01 a un servidor DNS d'internet:

```bash
profe@sx-cli-profe01:~$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=118 time=23.5 ms
```

### Configuració de les direccions dels servidors DNS

Encara que tenim connexió a internet a la màquina client, perquè hem habilitat l'encaminament al server, si tractem de resoldre un nom de domini al client, obtindrem un error:

```bash

profe@sx-cli-profe01:~$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=118 time=23.5 ms
```

És degut al fet que no hem configurat cap servidor DNS a la configuració de xarxa del client, i per tant no sap a on ha de demanar la resolució del nom de domini.&#x20;

Per a solucionar-ho, haurem d'editar el fitxer de configuració de netplan, i afegir la configuració corresponent als servidors DNS. Per a l'exemple afegirem els dos servidors DNS principals de Google (amb les IP 8.8.8.8 i 8.8.4.4):

```yaml
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
      addresses:
      - 192.168.0.101/24
      routes:
        - to: default
          via: 192.168.0.100
      nameservers:
        addresses:
        - 8.8.8.8
        - 8.8.4.4
      dhcp4: false

```

Recarreguem la configuració de xarxa al sistema:

```bash
profe@sx-cli-profe01:~$ sudo netplan apply
** (generate:2005): WARNING **: 17:21:46.349: `gateway4` has been deprecated, use default routes instead.
See the 'Default routes' section of the documentation for more details.
```

I tornem a provar la resolució de noms al client, comprovant que tot funciona correctament:

```bash
profe@sx-cli-profe01:~$ nslookup  www.google.com;
Server:         127.0.0.53
Address:        127.0.0.53#53

Non-authoritative answer:
Name:   www.google.com
Address: 142.250.185.4
Name:   www.google.com
Address: 2a00:1450:4003:803::2004

profe@sx-cli-profe01:~$ ping www.google.com;
PING www.google.com (142.250.184.4) 56(84) bytes of data.
64 bytes from mad41s10-in-f4.1e100.net (142.250.184.4): icmp_seq=1 ttl=118 time=22.9 ms
64 bytes from mad41s10-in-f4.1e100.net (142.250.184.4): icmp_seq=2 ttl=118 time=21.2 ms
```

Si obrim el navegador web del client, podrem accedir a la web de l'institut, publicada a internet, fent servir la màquina server com a proxy de connexió.

<figure><img src="../.gitbook/assets/image (1).png" alt=""><figcaption><p>Pàgina web visitada des de la màquina client, a través de la porta d'enllaç configurada a la xarxa 'aula'</p></figcaption></figure>
