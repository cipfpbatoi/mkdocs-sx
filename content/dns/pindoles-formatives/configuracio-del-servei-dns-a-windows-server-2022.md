---
description: Configuració del servei DNS a Windows Server 2022
---

# ⚒ Configuració del servei DNS a Windows Server 2022

Partim d'una màquina virtual, amb un sistema operatiu basat a Windows Server 2022, i que té configurades dues interfícies de xarxa:

* Una connectada a NAT, perquè el servidor tinga accés a internet i puga instal·lar paquets.

<figure><img src="../.gitbook/assets/image (3).png" alt=""><figcaption><p>Configuració de la interfície de xarxa de VirtualBox a NAT</p></figcaption></figure>

* Una connectada a la xarxa interna 'aula'.

<figure><img src="../.gitbook/assets/image (1).png" alt=""><figcaption><p>Configuració de la interfície de xarxa de VirtualBox a Xarxa interna 'aula'</p></figcaption></figure>

* [ ] Instal·lació del servei DNS&#x20;

Instal·lem el servei DNS a Windows, fent servir l'assistent de l'administrador del servidor, accedint a l'opció Administrar --> Agregar rols i característiques.

<figure><img src="../.gitbook/assets/image (29).png" alt=""><figcaption><p>Administrador del servidor.</p></figcaption></figure>

A l'assistent, avançarem pel mateix, seleccionant les opcions que veiem a les següents captures:&#x20;

<figure><img src="../.gitbook/assets/image (30).png" alt=""><figcaption><p>Inici de l'assistent per a agregar rols i característiques.</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (31).png" alt=""><figcaption><p>Selecció del tipus d'instal·lació basada en característiques o rols.</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (32).png" alt=""><figcaption><p>Selecció del servidor.</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (33).png" alt=""><figcaption><p>Selecció del servei a instal·lar.</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (34).png" alt=""><figcaption><p>Selecció de requisits necessaris per dur a terme la instal·lació</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (35).png" alt=""><figcaption><p>Continuación de la selecció de rols.</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (36).png" alt=""><figcaption><p>Revisió de les característiques del servidor.</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (37).png" alt=""><figcaption><p>Confirmació de la selecció del servei DNS.</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (38).png" alt=""><figcaption><p>Confirmació de selecció de reinici automàtic, si cal.</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (39).png" alt=""><figcaption><p>Progrés de la instal·lació.</p></figcaption></figure>

Una volta instal·lat el servei DNS, hem de configurar-lo, a l'opció 'Ferramentes --> DNS' de la finestra d'administració del servidor:

<figure><img src="../.gitbook/assets/image (40).png" alt=""><figcaption><p>Ferramenta de configuració del servei DNS.</p></figcaption></figure>

Ara podem crear una zona de cerca directa, y una de cerca inversa, per configurar les nostres DNS:

<figure><img src="../.gitbook/assets/image (41).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (42).png" alt=""><figcaption><p>Assistent per a crear una nova zona.</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (43).png" alt=""><figcaption><p>Creació d'una zona principal.</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (44).png" alt=""><figcaption><p>Configuració del nom de la zona</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (46).png" alt=""><figcaption><p>Creació del fitxer de configuració de zona.</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (47).png" alt=""><figcaption><p>Configuració per a no permetre les actualitzacions dinàmiques de la zona.</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (48).png" alt=""><figcaption><p>Revisió de les opcions de la zona.</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (51).png" alt=""><figcaption><p>Creació de zona inversa de cerca</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (52).png" alt=""><figcaption><p>Assistent per a nova zona</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (53).png" alt=""><figcaption><p>Creació d'una zona principal.</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (54).png" alt=""><figcaption><p>Selecció de zona IPv4</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (55).png" alt=""><figcaption><p>Configuració de la zona inversa</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (56).png" alt=""><figcaption><p>Creació del fitxer de zona inversa.</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (57).png" alt=""><figcaption><p>Configuració per a no permetre les actualitzacions dinàmiques de la zona.</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (58).png" alt=""><figcaption><p>Finalització de l'assistent de zona inversa</p></figcaption></figure>



Una volta creada la zona de cerca directa, i la zona de cerca inversa, podem afegir registres DNS al nostre servidor, per exemple, podem afegir un registre per a referenciar la intranet i la impressora de xarxa:

<figure><img src="../.gitbook/assets/image (49).png" alt=""><figcaption><p>Creació d'un nou registre A</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (50).png" alt=""><figcaption><p>Configuració de la DNS per a la intranet.</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (59).png" alt=""><figcaption><p>Configuració de la DNS per a la impressora.</p></figcaption></figure>

Podem comprovar la configuració al panel de control del servei DNS:

<figure><img src="../.gitbook/assets/image (60).png" alt=""><figcaption><p>DNS configurades</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (61).png" alt=""><figcaption><p>Punters de IP a DNS configurades.</p></figcaption></figure>

{% hint style="danger" %}
Per a poder provar el servei DNS configurat, haurem d'engegar un client, i configurar la seua tarjeta de xarxa, indicant que la IP del servei DNS siga la IP de la màquina que acabem de configurar.&#x20;
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
IP4.DOMAIN[1]:                          aula.local
IP6.ADDRESS[1]:                         fe80::a00:27ff:fe71:febd/64
IP6.GATEWAY:                            --
IP6.ROUTE[1]:                           dst = fe80::/64, nh = ::, mt = 256

```

A continuació, podem provar les resolucions de noms amb el comandament nslookup:

```bash
jorge@sx-cli-jorge-01:~$ nslookup intranet.aula.internal
Server:         127.0.0.53
Address:        127.0.0.53#53

Non-authoritative answer:
Name:   intranet.aula.internal
Address: 192.168.0.250

jorge@sx-cli-jorge-01:~$ nslookup impressora.aula.internal
Server:         127.0.0.53
Address:        127.0.0.53#53

Non-authoritative answer:
Name:   impressora.aula.internal
Address: 192.168.0.251

jorge@sx-cli-jorge-01:~$ nslookup www.google.com
Server:         127.0.0.53
Address:        127.0.0.53#53

Non-authoritative answer:
Name:   www.google.com
Address: 142.250.200.68
Name:   www.google.com
Address: 2a00:1450:4003:80d::2004
```

