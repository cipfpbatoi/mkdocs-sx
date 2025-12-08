---
description: Configuració de subzona al servei DNS a Ubuntu Server 24.04
---

# ⚒️ Configuració de subzona al servei DNS a Ubuntu 24.04

Partim de dues màquines virtual, amb un sistema operatiu basat a Ubuntu Server 24.04

### Configuració del servei DNS de zona del subdomini.

En primer lloc, configurarem el servidor DNS que actua com a servidor de zona del subdomini.

La màquina virtual d'aquest servidor té configurada una interfície de xarxa, connectada a la xarxa interna 'aula'.

<figure><img src="../.gitbook/assets/image (62).png" alt=""><figcaption><p>Configuració de xarxa interna.</p></figcaption></figure>

Obrim un terminal, per a fer les operacions de configuració:

* [ ] Configuració de la xarxa

Editem el fitxer de netplan, per indicar que el servidor de la zona del subdomini es troba a la IP 192.168.0.2

* [ ] Instal·lació del servei DNS bind9

Instal·lem el servei DNS a Ubuntu, la seua documentació i el paquet dnsutils.

```bash
profe@sx-srv-profe-dhcp:~$ sudo apt install bind9 bind9utils bind9-doc dnsutils
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following additional packages will be installed:
  bind9-dnsutils bind9-host bind9-libs bind9-utils dns-root-data liblmdb0 libmaxminddb0 libuv1
Suggested packages:
  bind-doc resolvconf mmdb-bin
The following NEW packages will be installed:
  bind9 bind9-dnsutils bind9-doc bind9-host bind9-libs bind9-utils dns-root-data dnsutils liblmdb0 libmaxminddb0 libuv1
0 upgraded, 11 newly installed, 0 to remove and 13 not upgraded.
Need to get 5240 kB of archives.
After this operation, 19.1 MB of additional disk space will be used.
Do you want to continue? [Y/n]
```

* [ ] Configuració general del servei DNS:

Editem el fitxer **/etc/bind/named.conf.options** per a configurar el acl de la xarxa, i els forwarders, si ho necessitem:

```bash
acl aula-internal-network {
        192.168.0.0/24;
};
options {
        directory "/var/cache/bind";

        allow-query { localhost; aula-internal-network; };
        allow-transfer { localhost; };

        // If there is a firewall between you and nameservers you want
        // to talk to, you may need to fix the firewall to allow multiple
        // ports to talk.  See http://www.kb.cert.org/vuls/id/800113

        // If your ISP provided one or more IP addresses for stable
        // nameservers, you probably want to use them as forwarders.
        // Uncomment the following block, and insert the addresses replacing
        // the all-0\'s placeholder.

        forwarders {
                8.8.8.8;
                8.8.4.4;
        };

        recursion yes;

        //========================================================================
        // If BIND logs error messages about the root key being expired,
        // you will need to update your keys.  See https://www.isc.org/bind-keys
        //========================================================================
        dnssec-validation no;

        listen-on-v6 { none; };
};
```

Podem actualitzar el fitxer **/etc/default/named** per indicar que ha d'escolar per defecte les peticions IPv4:

```bash
OPTIONS="-u bind -4"
```

* [ ] Configuració de una nova zona de subdomini (zona1.midominio.aula.):

Editem el fitxer **/etc/bind/named.conf.local**, per indicar les zones o dominis de resolució del servidor. Ací configurarem la zona zona1.midominio.aula, i la zona inversa 0.168.192, corresponent al rang de xarxa 192.168.0.x.

A les dues zones indicarem si el servei actuarà com a primari (master) o secundari (slave), així com el fitxer de configuració de la resolució:

```bash
// Configuració per al domini aula.internal
zone "zona1.midominio.aula" IN {
        type master;
        file "/etc/bind/forward.zona1.midominio.aula";
        allow-update { none; };
};

// Configuració per al rang 192.168.0.0/24
zone "0.168.192.in-addr.arpa" IN {
        type master;
        file "/etc/bind/reverse.zona1.midominio.aula";
        allow-update { none; };
};
```

* [ ] Configuració del fitxer de resolució directa:

Per a crear la nostra BD de resolució de noms, editem el fitxer **/etc/bind/forward.zona1.midominio.aula**, incluint els registres DNS de configuració de la zona del subdomini:

```bash
$TTL    30
@       IN      SOA     dns1.zona1.midominio.aula. admin.midominio.aula. (
                                2               ; Serial
                                604800          ; Refresh
                                86400           ; Retry
                                2419200         ; Expire
                                604800 )        ; Negative Cache TTL
;
$ORIGIN zona1.midominio.aula.
@       IN      NS      dns1
dns1    IN      A       192.168.0.2
intranet        IN      A       192.168.0.250
impresora       IN      A       192.168.0.251
printer         IN      CNAME   impresora.zona1.midominio.aula.

```

* [ ] Configuració del fitxer de resolució inversa:

Per a crear la nostra BD de resolució inversa d'IP, editem el fitxer **/etc/bind/reverse.zona1.midominio.aula**, incloent-hi els registres DNS de la nostra zona:

```bash
$TTL    30
@       IN      SOA     dns1.zona1.midominio.aula. admin.midominio.aula. (
                                1               ; Serial
                                604800          ; Refresh
                                86400           ; Retry
                                2419200         ; Expire
                                604800 )        ; Negative Cache TTL

; info del nameserver
        IN      NS      dns1.zona1.midominio.aula.
dns1    IN      A       192.168.0.2

; reverse loockup dns server
2       IN      PTR     dns1.zona1.midominio.aula.

; reverse loockup hosts
250     IN      PTR     intranet.zona1.midominio.aula.
251     IN      PTR     impresora.zona1.midominio.aula.
```

Comprovem que no hi ha errors als nostres fitxers de configuració:

```bash
profe@sx-srv-profe-dhcp:~$ sudo named-checkconf
```

Engeguem el servei:

```bash
profe@sx-srv-profe-dhcp: sudo service bind9 start;
profe@sx-srv-profe-dhcp: sudo service bind9 status;

profe@sx-srv-profe-dhcp: sudo systemctl enable named;
profe@sx-srv-profe-dhcp: sudo systemctl start named;
profe@sx-srv-profe-dhcp: sudo systemctl status named;
```

I configurem el tallafoc del servidor perquè habilite les connexions al servei Bind9:

```bash
profe@sx-srv-profe-dhcp:~$ sudo ufw allow Bind9;
profe@sx-srv-profe-dhcp:~$ sudo ufw reload;
profe@sx-srv-profe-dhcp:~$ sudo ufw disable;
profe@sx-srv-profe-dhcp:~$ sudo ufw enable;
profe@sx-srv-profe-dhcp:~$ sudo ufw status;
```

* [ ] Prova del servei configurat

Podem provar el servei, indicant a nslookup que ha de fer servir aquest servidor DNS com a servidor de resolució:

```
profe@sx-srv-profe-dhcp:~$ nslookup printer.zona1.midominio.aula 192.168.0.2
Server:         192.168.0.2
Address:        192.168.0.2#53

Name:   impresora.zona1.midominio.aula
Address: 192.168.0.251
```

{% hint style="danger" %}
Fins ara hem configurat el servidor del subdomini zona1.midominio.aula.

A continuació configurarem el servidor principal del domini midominio.com., que delegarà les peticions de resolució del subdomini a aquest servidor.
{% endhint %}

### Configuració del servei DNS de zona del domini principal.

A continuació, configurarem el servidor DNS que actua com a servidor de zona del domini principal.

La màquina virtual d'aquest servidor té configurades dues interfície de xarxa:

* Una connectada a NAT, perquè el servidor tinga accés a internet i puga instal·lar paquets.

<figure><img src="../.gitbook/assets/image (3).png" alt=""><figcaption><p>Configuració de la interfície de xarxa de VirtualBox a NAT</p></figcaption></figure>

* Una connectada a la xarxa interna 'aula'.

<figure><img src="../.gitbook/assets/image (62) (1).png" alt=""><figcaption><p>Configuració de la interfície de xarxa de VirtualBox a Xarxa interna 'aula'</p></figcaption></figure>

{% hint style="info" %}
Per a configurar routing, NAT i DHCP, podeu consultar els tutorials de les unitats anteriors.
{% endhint %}

Obrim un terminal, per a fer les operacions de configuració:

* [ ] Instal·lació del servei DNS

Instal·lem el servei DNS a Ubuntu, la seua documentació i el paquet dnsutils.

```bash
profe@sx-srv-profe-dhcp:~$ sudo apt install bind9 bind9utils bind9-doc dnsutils
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following additional packages will be installed:
  bind9-dnsutils bind9-host bind9-libs bind9-utils dns-root-data liblmdb0 libmaxminddb0 libuv1
Suggested packages:
  bind-doc resolvconf mmdb-bin
The following NEW packages will be installed:
  bind9 bind9-dnsutils bind9-doc bind9-host bind9-libs bind9-utils dns-root-data dnsutils liblmdb0 libmaxminddb0 libuv1
0 upgraded, 11 newly installed, 0 to remove and 13 not upgraded.
Need to get 5240 kB of archives.
After this operation, 19.1 MB of additional disk space will be used.
Do you want to continue? [Y/n]
```

* [ ] Configuració general del servei DNS:

Editem el fitxer **/etc/bind/named.conf.options** per a configurar el acl de la xarxa, i els forwarders, si ho necessitem:

```bash
acl aula-internal-network {
        192.168.0.0/24;
};
options {
        directory "/var/cache/bind";

        allow-query { localhost; aula-internal-network; };
        allow-transfer { localhost; };

        // If there is a firewall between you and nameservers you want
        // to talk to, you may need to fix the firewall to allow multiple
        // ports to talk.  See http://www.kb.cert.org/vuls/id/800113

        // If your ISP provided one or more IP addresses for stable
        // nameservers, you probably want to use them as forwarders.
        // Uncomment the following block, and insert the addresses replacing
        // the all-0\'s placeholder.

        forwarders {
                8.8.8.8;
                8.8.4.4;
        };

        recursion yes;

        //========================================================================
        // If BIND logs error messages about the root key being expired,
        // you will need to update your keys.  See https://www.isc.org/bind-keys
        //========================================================================
        dnssec-validation no;

        listen-on-v6 { none; };
};
```

Podem actualitzar el fitxer **/etc/default/named** per indicar que ha d'escolar per defecte les peticions IPv4:

```bash
OPTIONS="-u bind -4"
```

* [ ] Configuració de una nova zona de domini (midominio.aula.):

Editem el fitxer **/etc/bind/named.conf.local**, per indicar les zones o dominis de resolució del servidor. Ací configurarem:

* La zona midominio.aula
* La zona inversa 0.168.192, corresponent al rang de xarxa 192.168.0.x.
* La zona del subdomini. zona1.midominio.aula, indicant que és de tipo fordward, i indicant el servidor DNS de la zona delegada.

<pre class="language-bash"><code class="lang-bash">// Configuració per al domini aula.internal
zone "midominio.aula" IN {
        type master;
        file "/etc/bind/forward.midominio.aula";
        allow-update { none; };
};

<strong>// Configuració per al domini zona1.aula.internal
</strong><strong>zone "zona1.midominio.aula" IN {
</strong><strong>        type forward;
</strong><strong>        forwarders { 192.168.0.2; };
</strong><strong>};
</strong>
// Configuració per al rang 192.168.0.0/24
zone "0.168.192.in-addr.arpa" IN {
        type master;
        file "/etc/bind/reverse.midominio.aula";
        allow-update { none; };
};
</code></pre>

* [ ] Configuració del fitxer de resolució directa:

Per a crear la nostra BD de resolució de noms, editem el fitxer **/etc/bind/forward.midominio.aula**, incluint els registres DNS de configuració de la zona del subdomini:

```bash
$TTL    30
@       IN      SOA     dns1.midominio.aula. admin.midominio.aula. (
                                2               ; Serial
                                604800          ; Refresh
                                86400           ; Retry
                                2419200         ; Expire
                                604800 )        ; Negative Cache TTL
;
$ORIGIN midominio.aula.
@       IN      NS      dns1
dns1    IN      A       192.168.0.1
intranet        IN      A       192.168.0.150
impresora       IN      A       192.168.0.151
printer         IN      CNAME   impresora.midominio.aula.
;
$ORIGIN zona1.midominio.aula.
@       IN      NS      dns1
dns1    IN      A       192.168.0.2
```

* [ ] Configuració del fitxer de resolució inversa:

Per a crear la nostra BD de resolució inversa d'IP, editem el fitxer **/etc/bind/reverse.midominio.aula**, incloent-hi els registres DNS de la nostra zona:

```bash
$TTL    30
@       IN      SOA     dns1.midominio.aula. admin.midominio.aula. (
                                1               ; Serial
                                604800          ; Refresh
                                86400           ; Retry
                                2419200         ; Expire
                                604800 )        ; Negative Cache TTL

; info del nameserver
        IN      NS      dns1.midominio.aula.
dns1    IN      A       192.168.0.1

; reverse loockup dns server
1       IN      PTR     dns1.midominio.aula.
2       IN      PTR     dns1.zona1.midominio.aula.

; reverse loockup hosts
150     IN      PTR     intranet.midominio.aula.
151     IN      PTR     impresora.midominio.aula.
```

Comprovem que no hi ha errors als nostres fitxers de configuració:

```bash
profe@sx-srv-profe-dhcp:~$ sudo named-checkconf
```

Engeguem el servei:

```bash
profe@sx-srv-profe-dhcp: sudo service bind9 start;
profe@sx-srv-profe-dhcp: sudo service bind9 status;

profe@sx-srv-profe-dhcp: sudo systemctl enable named;
profe@sx-srv-profe-dhcp: sudo systemctl start named;
profe@sx-srv-profe-dhcp: sudo systemctl status named;
```

I configurem el tallafoc del servidor perquè habilite les connexions al servei Bind9:

```bash
profe@sx-srv-profe-dhcp:~$ sudo ufw allow Bind9;
profe@sx-srv-profe-dhcp:~$ sudo ufw reload;
profe@sx-srv-profe-dhcp:~$ sudo ufw disable;
profe@sx-srv-profe-dhcp:~$ sudo ufw enable;
profe@sx-srv-profe-dhcp:~$ sudo ufw status;
```

* [ ] Prova del servei configurat

Podem provar el servei, indicant a nslookup que ha de fer servir aquest servidor DNS com a servidor de resolució:

```
profe@sx-srv-profe-dhcp:~$ nslookup impresora.midominio.aula 192.168.0.1
Server:         192.168.0.1
Address:        192.168.0.1#53

Name:   impresora.midominio.aula
Address: 192.168.0.151

profe@sx-srv-profe-dhcp:~$ nslookup impresora.zona1.midominio.aula 192.168.0.1
Server:         192.168.0.1
Address:        192.168.0.1#53

Name:   impresora.zona1.midominio.aula
Address: 192.168.0.251
```

{% hint style="danger" %}
Ara podem resoldre les DNS del domini i del subdomini, fent servir el servidor del domini com a servidor DNS dels clients. Proba-ho!!
{% endhint %}

### Configuració utilitzant Servidors Delegats

Tot el que hem vist fins ara, ha sigut configurant els glue-records. Aquesta es la manera correcta de configurar-ho perquè gràcies a ella, podem escalar i mantindre el servidors adecuadament. Un altra opció, pot ser configurant la zona delegada i el servidor DNS delegat per al domini, per a realitzar aquesta configuració es pot fer de la següent manera:

Primer, afegim la configuració de zona del servidor, la zona delegada

```bash
// Configuració per al domini zona1.aula.internal
zone "zona1.midominio.aula" IN {
        type forward;
        forwarders { 192.168.0.2; };
};
```

I després afegim els registres al DNS principal.

```bash
; Delegacion de Zona
ext.aula.internal.        IN NS   dns1.ext.aula.internal.
dns1.ext.aula.internal.   IN A    192.168.0.3
```
