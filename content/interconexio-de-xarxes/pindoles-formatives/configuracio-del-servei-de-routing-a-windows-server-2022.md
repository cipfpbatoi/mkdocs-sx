---
description: Configuració del servei de routing i NAT a Windows server 2022
---

# ⚒ Configuració del servei de routing a Windows Server 2022

### Escenari inicial:

En aquest exemple, partim d'una configuració de xarxa com la mostrada a la següent imatge:

<figure><img src="../.gitbook/assets/UD00P01. esquema de red a configurar.png" alt=""><figcaption></figcaption></figure>

Suposem configurades les targetes de xarxa interna de les màquines virtuals, amb IP fixa, dins de la xarxa 192.168.0.0/24.

Les màquines clients disposaran d'una IP a partir de la 192.168.0.101.

La màquina server, configurada amb un sistema operatiu basat a Windows Server, disposarà de dues targetes de xarxa:

* La primera configurada a la xarxa aula, amb la IP fixa 192.168.0.1. Aquesta interfície de xarxa treballarà com a porta d'enllaç per a connectar a internet a les màquines de la xarxa aula que ho necessiten.&#x20;
* La segona configurada com a xarxa NAT o Bridge, i assignació d'IP amb protocol DCHP.

Totes les màquines de la xarxa aula poden comunicar-se internament (podem executar un ping i funciona correctament).

### Habilitar les funcionalitats de routing i NAT en la màquina sx-winsrv-xxxx-01:

* [ ] Configuració dels paràmetres de les targetes de xarxa.

Hem de configurar la xarxa lògica, a Windows Server, obrint les opcions de configuració de xarxa de Windows.

<figure><img src="../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>

Seleccionem l'opció 'Ethernet', i a continuació l'opció 'caviar opcions de l'adaptador'&#x20;

<figure><img src="../.gitbook/assets/image (3).png" alt=""><figcaption></figcaption></figure>

Comprovem que la primera targeta de xarxa està configurada amb IP dinàmica (en VirtualBox l'hem configurada com a NAT):

<figure><img src="../.gitbook/assets/image (4).png" alt=""><figcaption></figcaption></figure>

Configurem la segona targeta de xarxa amb la IP desitjada, de manera estàtica, donat que és la targeta connectada a la xarxa interna aula. No cal configurar porta d'enllaç, perquè és la mateixa màquina, ni servidor DNS, perquè farà servir els rebuts per la configuració DHCP de l'altra targeta de xarxa.

<figure><img src="../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>

* [ ] Instal·lació del servei de routing

Obrim l'administrador del servidor, i dins del menú administrar, seleccionem l'opció 'afegir característiques'

<figure><img src="../.gitbook/assets/image (6).png" alt=""><figcaption></figcaption></figure>

Seguim les instruccions, per instal·lar el servei:

<figure><img src="../.gitbook/assets/image (7).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (8).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (9).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (10).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (11).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (12).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (13).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (14).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (15).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (16).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (17).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (18).png" alt=""><figcaption></figcaption></figure>

Quan finalitze la instal·lació podrem accedir a les noves funcionalitats, al menú 'ferramentes', pulsant sobre l'opció 'encaminament i accés remot':

<figure><img src="../.gitbook/assets/image (19).png" alt=""><figcaption></figcaption></figure>

En la finestra oberta, seleccionem el servei, polsem botó dret, i executem l'opció 'configurar i habilitat l'encaminament i l'accés remot':

<figure><img src="../.gitbook/assets/image (20).png" alt=""><figcaption></figcaption></figure>

I seguim les instruccions de l'assistent.

<figure><img src="../.gitbook/assets/image (21).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (22).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (23).png" alt=""><figcaption></figcaption></figure>

{% hint style="danger" %}
Si la següent opció no ens permet sel·leccionar la targeta de xarxa que està connectada a internet, hem de tancar l'assistent i tornar a llançar-lo.
{% endhint %}

<figure><img src="../.gitbook/assets/image (24).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (25).png" alt=""><figcaption></figcaption></figure>

Ara podríem configurar una màquina client per fer servir aquest servidor com a porta d'enllaç, i comprovar el correcte funcionament.
