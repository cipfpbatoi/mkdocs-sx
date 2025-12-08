---
description: Configuració dels grups de seguretat
---

# ⚒ Configuració dels grups de seguretat

Els grups de seguretat d'AWS són les regles que regulen el tràfic de xarxa a les xarxes virtuals del nostre entorn de treball, limitant o permitent el tràfic de xarxa de les màquines virtuals configurades.

Ens permet configurar tant el tràfic d'entrada com el tràfic d'eixida de les nostres màquines virtuals

Per a poder configurar les regles de xarxa, hem d'accedir al panel d'EC2:

<figure><img src="../../.gitbook/assets/image (115).png" alt=""><figcaption><p>Accés al panel d'EC2</p></figcaption></figure>

Una volta ens trobem al panell d'EC2, hem de buscar l'opció 'Security Groups' al menú lateral, a l'esquerra:

<figure><img src="../../.gitbook/assets/image (116).png" alt=""><figcaption><p>Accés a la pàgina de configuració dels security groups</p></figcaption></figure>

En carregar la pàgina, podrem observar els diferents security groups configurats.&#x20;

<figure><img src="../../.gitbook/assets/image (118).png" alt=""><figcaption><p>Llistat de security groups configurats</p></figcaption></figure>

Si volem crear un nou security group, polsarem el botó 'crear grup de seguretat':

<figure><img src="../../.gitbook/assets/image (119).png" alt=""><figcaption><p>Creació d'un nou security group</p></figcaption></figure>

Omplim les dades d'identificació del security group (nom i descripció):

<figure><img src="../../.gitbook/assets/image (120).png" alt=""><figcaption><p>Configuració del nom i la descripció</p></figcaption></figure>

Al panell de regles d'entrada podrem afegir totes les regles de tràfic entrant (definint els ports que obrirem a les màquines virtuals que apliquen el security group):

<figure><img src="../../.gitbook/assets/image (122).png" alt=""><figcaption><p>Regles de tràfic entrant</p></figcaption></figure>

A cada regla, definirem el protocol (TCP | UDP | ICMP) i el port o ports que volem obrir, així com l'origen de les peticions a les quals es permetrà l'accés.

Per exemple, podem configurar l'obertura del port TCP/22 (SSH) des de qualsevol IP (incloses IP públiques), de la següent manera:

<figure><img src="../../.gitbook/assets/image (123).png" alt=""><figcaption><p>Configuració de regla  d'entrada al security group</p></figcaption></figure>

O podem configurar l'obertura del port TCP/22 (SSH) des de qualsevol host que apliqui una altra regla preexistent al security group.

La següent regla permet el tràfic TCP/22 (SSH) des de qualsevol màquina que apliqui la regla ssh-bastion.

<figure><img src="../../.gitbook/assets/image (124).png" alt=""><figcaption><p>Configuració de regla d'entrada al security group</p></figcaption></figure>

De la mateixa manera, podem configurar regles d'eixida, per controlar a quins serveis podran connectar-se les màquines virtuals que apliquen la regla.&#x20;

La següent regla permet tot el tràfic d'eixida, cap a qualsevol desti i port.

<figure><img src="../../.gitbook/assets/image (125).png" alt=""><figcaption><p>Configuració de regla d'eixida al security group</p></figcaption></figure>

Una volta configurat el nostre security group, polsem sobre el botó 'Crear grup de seguretat', al final del formulari.

<figure><img src="../../.gitbook/assets/image (126).png" alt=""><figcaption></figcaption></figure>

Tornarem al llistat de regles de seguretat, on estarà disponible la nova regla.&#x20;

