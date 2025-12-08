---
description: Configuració del servei DNS a Ubuntu Server 24.04
---

# ⚒️ Configuració del servei DNS a Ubuntu 24.04

Partim d'una màquina virtual, amb un sistema operatiu basat a Ubuntu Server 24.04, i que té configurades dues interfícies de xarxa:

* Una connectada a NAT, perquè el servidor tinga accés a internet i puga instal·lar paquets.

<figure><img src=".gitbook/assets/image (3).png" alt=""><figcaption><p>Configuració de la interfície de xarxa de VirtualBox a NAT</p></figcaption></figure>

* Una connectada a la xarxa interna 'aula'.

<figure><img src=".gitbook/assets/image (1).png" alt=""><figcaption><p>Configuració de la interfície de xarxa de VirtualBox a Xarxa interna 'aula'</p></figcaption></figure>

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

Recordem els comandaments per arrancar, parar, reiniciar, recarregar la configuració i consultar l'estat del servei, així com el comandament de reinici o recàrrega de configuració:

```bash
sudo systemctl [enable|start|stop|restart|reload|status] bind9;
```

També podem fer servir els comandaments corresponents, fent servir systemctl, per activar, arrancar, parar, reiniciar, recarregar la configuració i consultar l'estat del servei:

```bash
sudo systemctl [enable|start|stop|restart|reload|status] named;
```

* [ ] Configuració general del servei DNS:

Editem el fitxer **/etc/bind/named.conf.options**. En aquest fitxer podem:

* Habilitar la consulta al teu DNS des de la teva xarxa privada (Com el seu nom indica, només els sistemes de la teva xarxa privada poden consultar DNS sever per nom a traducció IP i viceversa).
* Configurar el reenviament de consultes (la consulta DNS es reenviarà als reenviadors quan el servidor DNS local no pugui resoldre la consulta).
* Habilitar la consulta recursiva.

El nostre fitxer quedarà així, si volem configurar el domini aula.internal, al ran de xarxa 192.168.0.0/24:

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

* [ ] Configuració de una nova zona de domini (aula.internal.):

Editem el fitxer **/etc/bind/named.conf.local**, per indicar les zones o dominis de resolució del servidor. Ací configurarem la zona aula.internal, i la zona inversa 0.168.192, corresponent al rang de xarxa 192.168.0.x.

A les dues zones indicarem si el servei actuarà com a primari (master) o secundari (slave), així com el fitxer de configuració de la resolució:

```bash
// Configuració per al domini aula.internal
zone "aula.internal" IN {
        type master;
        file "/etc/bind/forward.aula.internal";
        allow-update { none; };
};

// Configuració per al rang 192.168.0.0/24
zone "0.168.192.in-addr.arpa" IN {
        type master;
        file "/etc/bind/reverse.aula.internal";
        allow-update { none; };
};
```

* [ ] Configuració del fitxer de resolució directa:

Per a crear la nostra BD de resolució de noms, copiem el fitxer **/etc/bind/db.local** com **/etc/bind/forward.aula.internal**, per fer-lo servir de plantilla, i editem el mateix en les dades del nostre domini:

```bash
$TTL    30
@       IN      SOA     dns1.aula.internal. admin.aula.internal. (
                                2               ; Serial
                                604800          ; Refresh
                                86400           ; Retry
                                2419200         ; Expire
                                604800 )        ; Negative Cache TTL
;

        IN      NS      dns1.aula.internal.
dns1    IN      A       192.168.0.1

gateway IN      A       192.168.0.1
dhcp    IN      A       192.168.0.1

intranet        IN      A       192.168.0.200
impresora       IN      A       192.168.0.250
```

Explicació detallada de la configuració aplicada, directiva a directiva:

```bash
$TTL    30
```

* TTL (Time To Live): Estableix el temps de vida de les respostes del servidor DNS, per aquesta zona. En aquest cas, 30 segons. Si un client fa una consulta referent a la zona configurada, la resposta té una validesa de 30 segons.

```bash
@       IN      SOA     dns1.aula.internal. admin.aula.internal. (       
                                2               ; Serial                 
                                604800          ; Refresh                
                                86400           ; Retry                  
                                2419200         ; Expire                 
                                604800 )        ; Negative Cache TTL     
;   
```

* Registre **SOA** (Start of Authority):
  * L'**@** referència al nivell principal de la zona que estem configurant, indicada al fitxer **/etc/bind/named.conf.internal(aula.internal.)**
  * **SOA** indica que estem configurant el servidor DNS autoritary de la zona.
  * dns1.aula.internal. indica la DNS del servidor
  * admin.aula.internal. Indica el correu electrònic de l'administrador (el primer punt substitueix l'@ del correu).
  * La resta de camps numèrics són:
    1. **2**: Aquest és el número de sèrie. Es recomana incrementar aquest número cada vegada que es realitza un canvi a la zona per facilitar la propagació de la informació.
    2. **604800**: Temps de refresc. Indica cada quants segons han de comprovar altres servidors DNS si hi ha hagut canvis al servidor primari.
    3. **86400**: Temps de reintent. Indica quant de temps esperar abans de provar de nou si un intent de comunicació falla.
    4. **2419200**: Temps d'expiració. Indica quant de temps un servidor secundari pot mantenir la seva còpia de la zona sense actualitzar abans de considerar-la obsoleta.
    5. **604800**: Temps de vida de la memòria cau negativa (Negative Cache TTL). Indica quant de temps un servidor ha de mantenir en memòria cau les respostes negatives (com ara "no s'ha trobat") abans de consultar de nou el servidor primari.

```bash
        IN      NS      dns1.aula.internal.                              
dns     IN      A       192.168.0.1 
```

* **NS** indica que estem configurant la direcció del servidor DNS del domini.
* **dns1.aula.internal.** Indica la direcció del servidor.
* La resolució del nom **'dns'** de la zona (.aula.internal.) es correspon amb la IP **192.168.0.1.**

```bash
gateway IN      A       192.168.0.1                                      
dhcp    IN      A       192.168.0.1                                      
```

* Estem configurant tres registres A, o de resolució de nom a IP, que apunten a la mateixa IP destí. Amb ells hem indicat que:
  * La resolució del nom **'dns'** de la zona (.aula.internal.) es correspon amb la IP 192.168.0.1.
  * La resolució del nom **'gateway'** de la zona (.aula.internal.) es correspon amb la IP 192.168.0.1.
  * La resolució del nom **'dhcp'** de la zona (.aula.internal.) es correspon amb la IP 192.168.0.1.

```bash
intranet        IN      A       192.168.0.200                            
impresora       IN      A       192.168.0.250
```

* Estem configurant dos registres A, o de resolució de nom a IP, que apunten a dos host de la nostra zona DNS. Amb ells hem indicat que:
  * La resolució del nom **'intranet'** de la zona (.aula.internal.) es correspon amb la IP 192.168.0.200.
  * La resolució del nom **'impresora'** de la zona (.aula.internal.) es correspon amb la IP 192.168.0.250.

- [ ] Configuració del fitxer de resolució inversa:

Per a crear la nostra BD de resolució inversa d'IP, copiem el fitxer **/etc/bind/db.127** com **/etc/bind/reverse.aula.internal**, per fer-lo servir de plantilla, i editem el mateix en les dades del nostre domini:

```bash
$TTL    30
@       IN      SOA     dns1.aula.internal. admin.aula.internal. (
                                1               ; Serial
                                604800          ; Refresh
                                86400           ; Retry
                                2419200         ; Expire
                                604800 )        ; Negative Cache TTL

; info del nameserver
        IN      NS      dns1.aula.internal.
dns1    IN      A       192.168.0.1

; reverse loockup dns server
1       IN      PTR     dns1.aula.internal.

; reverse loockup hosts
200     IN      PTR     intranet.aula.internal.
250     IN      PTR     impresora.aula.internal.
```

Explicació detallada de la configuració aplicada, directiva a directiva:

```bash
$TTL   30
```

* TTL (Time To Live): Estableix el temps de vida de les respostes del servidor DNS, per aquesta zona. En aquest cas, 30 segons. Si un client fa una consulta referent a la zona configurada, la resposta té una validesa de 30 segons.

```bash
@       IN      SOA     dns1.aula.internal. admin.aula.internal. (
                                1               ; Serial
                                604800          ; Refresh
                                86400           ; Retry
                                2419200         ; Expire
                                604800 )        ; Negative Cache TTL
```

* Registre **SOA** (Start of Authority):
  * L'**@** referència al nivell principal de la zona que estem configurant, indicada al fitxer **/etc/bind/named.conf.internal(aula.internal.)**
  * **SOA** indica que estem configurant el servidor DNS autoritary de la zona.
  * dns1.aula.internal. indica la DNS del servidor
  * admin.aula.internal. Indica el correu electrònic de l'administrador (el primer punt substitueix l'@ del correu).
  * La resta de camps numèrics són:
    1. **2**: Aquest és el número de sèrie. Es recomana incrementar aquest número cada vegada que es realitza un canvi a la zona per facilitar la propagació de la informació.
    2. **604800**: Temps de refresc. Indica cada quants segons han de comprovar altres servidors DNS si hi ha hagut canvis al servidor primari.
    3. **86400**: Temps de reintent. Indica quant de temps esperar abans de provar de nou si un intent de comunicació falla.
    4. **2419200**: Temps d'expiració. Indica quant de temps un servidor secundari pot mantenir la seva còpia de la zona sense actualitzar abans de considerar-la obsoleta.
    5. **604800**: Temps de vida de la memòria cau negativa (Negative Cache TTL). Indica quant de temps un servidor ha de mantenir en memòria cau les respostes negatives (com ara "no s'ha trobat") abans de consultar de nou el servidor primari.

```bash
; info del nameserver
        IN      NS      dns1.aula.internal.
dns1    IN      A       192.168.0.1
```

* **@** referència al domini de la zona que estem configurant, **NS** indica que estem configurant la direcció del servidor DNS del domini i **dns1.aula.internal.** indica la dns de resoluició del nameserver.
* **192.168.0.1** indica la IP de la dns **dns1** de la zona configurada (.aula.internal.)

```bash
; reverse loockup dns server
1       IN      PTR     dns1.aula.internal.
```

* La IP 1 del rang de xarxa configurat al fitxer de resolució inversa correspon a la DNS dns1.aula.internal.

```bash
; reverse loockup hosts
200     IN      PTR     intranet.aula.internal.
250     IN      PTR     impresora.aula.internal.
```

* La IP 200 del rang de xarxa configurat al fitxer de resolució inversa correspon a la DNS intranet.aula.internal.
* La IP 250 del rang de xarxa configurat al fitxer de resolució inversa correspon a la DNS impresora.aula.internal.

Comprovem que no hi ha errors als nostres fitxers de configuració:

```bash
profe@sx-srv-profe-dhcp:~$ sudo named-checkconf
```

Engeguem el servei:

```bash
## Bind9
profe@sx-srv-profe-dhcp: sudo systemctl restart bind9;
profe@sx-srv-profe-dhcp: sudo systemctl restart bind9;
## named 
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

{% hint style="danger" %}
Per a poder provar el servei DNS configurat, haurem d'engegar un client, i configurar la seua tarjeta de xarxa, indicant que la IP del servei DNS siga la IP de la màquina que acabem de configurar.

Si estem fent servir un servidor DNS, haurem de modificar els seus paràmertes, i reiniciar el servei, perque els clients puguen rebre la configuració correcta.
{% endhint %}

Comprovem la configuració de la xarxa:

```bash
jorge@sx-cli-jorge-02:~$ nmcli device show enp0s3
GENERAL.DEVICE:                         enp0s3
GENERAL.TYPE:                           ethernet
GENERAL.HWADDR:                         08:00:27:71:FE:BD
GENERAL.MTU:                            1500
GENERAL.STATE:                          100 (conectado)
GENERAL.CONNECTION:                     netplan-enp0s3
GENERAL.CON-PATH:                       /org/freedesktop/NetworkManager/Acti>
WIRED-PROPERTIES.CARRIER:               activado
IP4.ADDRESS[1]:                         192.168.0.151/24
IP4.GATEWAY:                            192.168.0.1
IP4.ROUTE[1]:                           dst = 192.168.0.0/24, nh = 0.0.0.0, >
IP4.ROUTE[2]:                           dst = 0.0.0.0/0, nh = 192.168.0.1, m>
IP4.DNS[1]:                             192.168.0.1
IP4.DOMAIN[1]:                          aula.internal
IP6.ADDRESS[1]:                         fe80::a00:27ff:fe71:febd/64
IP6.GATEWAY:                            --
IP6.ROUTE[1]:                           dst = fe80::/64, nh = ::, mt = 256

```

A continuació, podem probar les resolucions de noms amb el comandament dig:

```bash
jorge@sx-cli-jorge-01:~$ nslookup intranet
Server:         127.0.0.53
Address:        127.0.0.53#53

Non-authoritative answer:
Name:   intranet.aula.internal
Address: 192.168.0.200

jorge@sx-cli-jorge-01:~$ nslookup impresora
Server:         127.0.0.53
Address:        127.0.0.53#53

Non-authoritative answer:
Name:   impresora.aula.internal
Address: 192.168.0.250

```

{% hint style="warning" %}
En el cas de que no funcioni, tracteu de reiniciar el servei bind9, i comproveu l'estat del mateix, per si mostra algún error, com puga ser el següent:
{% endhint %}

<pre class="language-bash"><code class="lang-bash">profe@sx-srv-profe-dhcp:~$ sudo service bind9 restart;
profe@sx-srv-profe-dhcp:~$ sudo service bind9 status;
● named.service - BIND Domain Name Server
     Loaded: loaded (/lib/systemd/system/named.service; enabled; vendor preset: enabled)
     Active: active (running) since Sun 2023-10-22 14:53:22 UTC; 1s ago
       Docs: man:named(8)
    Process: 2180 ExecStart=/usr/sbin/named $OPTIONS (code=exited, status=0/SUCCESS)
   Main PID: 2181 (named)
      Tasks: 6 (limit: 4558)
     Memory: 6.0M
        CPU: 98ms
     CGroup: /system.slice/named.service
             └─2181 /usr/sbin/named -u bind -4

Oct 22 14:53:22 sx-srv-profe-dhcp named[2181]: zone 0.168.192.in-addr.arpa/IN: loaded serial 1
Oct 22 14:53:22 sx-srv-profe-dhcp named[2181]: zone 0.in-addr.arpa/IN: loaded serial 1
Oct 22 14:53:22 sx-srv-profe-dhcp named[2181]: zone aula.internal/IN: <a data-footnote-ref href="#user-content-fn-1">NS 'dns1.aula.internal' has no address records (A or AAAA)</a>
Oct 22 14:53:22 sx-srv-profe-dhcp named[2181]: zone aula.internal/IN: not loaded due to errors.
Oct 22 14:53:22 sx-srv-profe-dhcp named[2181]: zone 255.in-addr.arpa/IN: loaded serial 1
Oct 22 14:53:22 sx-srv-profe-dhcp named[2181]: zone localhost/IN: loaded serial 2
Oct 22 14:53:22 sx-srv-profe-dhcp named[2181]: zone 127.in-addr.arpa/IN: loaded serial 1
Oct 22 14:53:22 sx-srv-profe-dhcp named[2181]: all zones loaded
Oct 22 14:53:22 sx-srv-profe-dhcp systemd[1]: Started BIND Domain Name Server.
Oct 22 14:53:22 sx-srv-profe-dhcp named[2181]: running
</code></pre>

[^1]: Error en la configuració del registre dns1.aula.internal
