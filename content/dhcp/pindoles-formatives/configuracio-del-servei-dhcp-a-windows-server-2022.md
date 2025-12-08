---
description: Configuració del servei DHCP a Windows Server 2023
---

# ⚒ Configuració del servei DHCP a Windows Server 2022

Partim d'una màquina virtual, amb un sistema operatiu basat a Windows Server 2022, i que té configurades dues interfícies de xarxa:

* Una connectada a NAT, perquè el servidor tinga accés a internet i puga instal·lar paquets.

<figure><img src="../.gitbook/assets/image (3).png" alt=""><figcaption><p>Configuració de la interfície de xarxa de VirtualBox a NAT</p></figcaption></figure>

* Una connectada a la xarxa interna 'aula'.

<figure><img src="../.gitbook/assets/image (1).png" alt=""><figcaption><p>Configuració de la interfície de xarxa de VirtualBox a Xarxa interna 'aula'</p></figcaption></figure>

### Habilitar les funcionalitats de servidor DHCP en la màquina sx-winsrv-xxxx-01:

* [ ] Instal·lació del servei DHCP

Obrim l'administrador del servidor, i dins del menú administrar, seleccionem l'opció 'afegir característiques'

<figure><img src="../.gitbook/assets/image (4).png" alt=""><figcaption></figcaption></figure>

Seguim les instruccions, per instal·lar el servei:

<figure><img src="../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (6).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (7).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (8).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (9).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (10).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (11).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (12).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (13).png" alt=""><figcaption></figcaption></figure>

Esperem que finalitze la instal·lació, i tanquem la finestra d'administració:

<figure><img src="../.gitbook/assets/image (14).png" alt=""><figcaption></figcaption></figure>

Quan finalitze la instal·lació podrem accedir a les noves funcionalitats, al menú 'ferramentes', polsant sobre l'opció 'DHCP':

<figure><img src="../.gitbook/assets/image (15).png" alt=""><figcaption></figcaption></figure>

Ens obrirà la finestra de configuració del servei. Hem de polsar amb el botó dret a l'opció IPV4, i polsar sobre l'opció 'nou àmbit':

<figure><img src="../.gitbook/assets/image (16).png" alt=""><figcaption></figcaption></figure>

Ens obrirà un nou assistent, per configurar els paràmetres del servei DHCP. Hem de seguir les instruccions:

<figure><img src="../.gitbook/assets/image (17).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (18).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (19).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (20).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (21).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (22).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (23).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (24).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (25).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (26).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (27).png" alt=""><figcaption></figcaption></figure>

Apliquem  i esperem que el servidor carregue la nova configuració. Ja podem connectar nous clients a la nostra xarxa, amb l'opció de configuració de xarxa dinàmicament per DHCP, i el servei de Windows Server els proporcionarà els paràmetres de configuració afegits al nou àmbit.&#x20;

Quan un client sol·licite la configuració de xarxa, quedarà registrada la petició, i podrem observar tots els clients configurats per DHCP  a l'opció 'concessions de direccions':

<figure><img src="../.gitbook/assets/image (28).png" alt=""><figcaption></figcaption></figure>

Així mateix, podrem reservar adreces IP a l'opció 'reserves', indicant la direcció MAC de la targeta de xarxa, i la IP a reservar (com fem a la configuració de la xarxa de l'aula).

