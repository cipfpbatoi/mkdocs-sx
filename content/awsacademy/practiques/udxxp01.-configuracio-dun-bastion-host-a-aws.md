---
description: Configuració d'un host bastió a AWS
---

# 📎 UDXXP01.- Configuració d'un bastion host a AWS

## Objectiu

L'objectiu de la pràctica és configurar un host bastió a AWS, amb accés SSH des d'internet, per poder administrar la nostra infraestructura en el núvol.

### Requisits:

En primer lloc, configurarem dos grups de seguretat:

* ssh-internet: permetrà connectar des d'internet al port 22 de les instàncies EC2 que apliquen el grup de seguretat.
* Internet: permetrà l'accés a internet des de les instàncies EC2 que apliquen el grup de seguretat.

Posteriorment, desplegarem una instància EC2, configurada amb els grups de seguretat definits, i amb el sistema operatiu Ubuntu Server 24.04.

Una volta configurat el servei SSH a la nova instància, podrem connectar amb el nostre client SSH favorit:

### Creació dels grups de seguretat:&#x20;

Accedim al panell d'EC2, al nostre compte d'AWS academy:

<figure><img src="../.gitbook/assets/image (8).png" alt=""><figcaption><p>Cerca d'EC2 al cercador de serveis.</p></figcaption></figure>

Dins del panell d'EC2, busquem l'opció "Security Groups", al menú de l'esquerra.

<figure><img src="../.gitbook/assets/image (1) (1).png" alt=""><figcaption><p>Accés a l'opció "Security Groups"</p></figcaption></figure>

Dins de la pàgina de grups de seguretat, polsem el botó "Crear nou grup de seguretat".

<figure><img src="../.gitbook/assets/image (2) (1).png" alt=""><figcaption><p>Creació d'un nou grup de seguretat.</p></figcaption></figure>

Introduïm les dades bàsiques del grup de seguretat 'internet'.

<figure><img src="../.gitbook/assets/image (127).png" alt=""><figcaption><p>Dades bàsiques del grup de seguretat</p></figcaption></figure>

Deixem les regles d'entrada buides.

<figure><img src="../.gitbook/assets/image (128).png" alt=""><figcaption><p>Sense regles d'entrada</p></figcaption></figure>

Configurem la regla d'eixida, per a permetre la navegació a qualsevol IP/port.

<figure><img src="../.gitbook/assets/image (129).png" alt=""><figcaption><p>Regla d'eixida 0.0.0.0/0</p></figcaption></figure>

I polsem sobre el botó 'Crear grup de seguretat'.

<figure><img src="../.gitbook/assets/image (130).png" alt=""><figcaption><p>Confirmació de la creació del grup de seguretat.</p></figcaption></figure>

Tornarem al llistat de grups de seguretat, i tornem a crear sobre el botó 'Crear grup de seguretat'.

<figure><img src="../.gitbook/assets/image (131).png" alt=""><figcaption><p>Creació d'un nou grup de seguretat.</p></figcaption></figure>

Introduïm les dades bàsiques del grup de seguretat 'ssh-internet'.

<figure><img src="../.gitbook/assets/image (132).png" alt=""><figcaption><p>Dades bàsiques del grup de seguretat</p></figcaption></figure>

Configurem la regla d'entrada, per a permetre l'accés al port 22 des de qualsevol IP.

<figure><img src="../.gitbook/assets/image (133).png" alt=""><figcaption><p>Regla d'entrada SSH (TCP/22) des de 0.0.0.0/0</p></figcaption></figure>

Deixem les regles d'eixida buides, i polsem sobre el botó 'Crear grup de seguretat'.

<figure><img src="../.gitbook/assets/image (134).png" alt=""><figcaption><p>Confirmació de la creació del grup de seguretat.</p></figcaption></figure>

Tornarem al llistat de grups de seguretat, on podrem comprovar que tenim les noves regles definides.

### Creació del host bastió:&#x20;

A continuació, polsem sobre l'opció 'instàncies' al menú lateral esquerre.

<figure><img src="../.gitbook/assets/image (135).png" alt=""><figcaption><p>Llistat de grups de seguretat, i opció 'instàncies'</p></figcaption></figure>

Accedirem a la pàgina d'instàncies EC2 desplegades al nostre compte d'AWS Academy, i podrem polsar sobre el botó 'Llançar instància', per configurar el nostre host bastió.

<figure><img src="../.gitbook/assets/image (137).png" alt=""><figcaption><p>Opció 'llançar una nova instància'.</p></figcaption></figure>

En el formulari de creació d'instàncies, configurem el nom de la instància.

<figure><img src="../.gitbook/assets/image (138).png" alt=""><figcaption><p>Configuració de la instància.</p></figcaption></figure>

A continuació devem seleccionar l'AMI (Amazon Machine Image), amb la que s'inicialitzarà la instància EC2, configurada amb un sistema operatiu i programari base. En aquest cas, configurada amb Ubuntu 24.04 LTS, amb el servei OpenSSH.

<figure><img src="../.gitbook/assets/image (139).png" alt=""><figcaption><p>Selecció d'AMI</p></figcaption></figure>

Seleccionem el tipus d'instància, que determinarà la capacitat de procés i memòria. Al nostre cas farem servir una instància t2.micro, amb 1 CPU virtual i 1 GB de memòria.

<figure><img src="../.gitbook/assets/image (140).png" alt=""><figcaption><p>Selecció del tipus d'instància.</p></figcaption></figure>

I seleccionarem el parell de claus amb el que connectarem a la instància.&#x20;

<figure><img src="../.gitbook/assets/image (141).png" alt=""><figcaption><p>Selecció del parell de claus per autenticar l'administrador</p></figcaption></figure>

{% hint style="info" %}
Si encara no hem creat i descarregat un parell de claus, haurem de fer-ho abans de seleccionar-les.
{% endhint %}

{% hint style="danger" %}
Una volta generades les claus, i descarregades, haurem de tindre cura amb la custòdia d'aquestes, perquè seran necessàries per a connectar amb la instància configurada.&#x20;
{% endhint %}

Seleccionem els grups de seguretat a aplicar a la nova instància, que hem creat anteriorment (internet i ssh-internet).

<figure><img src="../.gitbook/assets/image (142).png" alt=""><figcaption><p>Selecció dels grups de seguretat</p></figcaption></figure>

{% hint style="info" %}
Recordem que els grups de seguretat actuen com a regles de filtrat de tràfic de xarxa, a la nostra infraestructura virtual.
{% endhint %}

I llancem la instància, polsant el botó corresponent.

<figure><img src="../.gitbook/assets/image (143).png" alt=""><figcaption><p>Llançament de la instància</p></figcaption></figure>

En llançar la instància, tornarem al llistat d'instàncies en execució del panell EC2, a on podrem seleccionar l'estat de la instància, i podrem seleccionar-la, per obtindre les dades de connexió.

<figure><img src="../.gitbook/assets/image (145).png" alt=""><figcaption><p>Detall de la instància desplegada.</p></figcaption></figure>

{% hint style="warning" %}
Recordatori: per a connectar amb clau privada a les instancies Ubuntu Server a AWS, hem de fer servir l'usuari ubuntu, com al següent exemple:

ssh -i /path/to/private-key ubuntu@ip-publica
{% endhint %}

{% hint style="danger" %}
Per a poder connectar, la clau privada ha de tindre aplicat permisos de soles lectura, i soles per a l'usuari:

chmod 400 /path/to/private-key
{% endhint %}



### Format de l'entrega

* L'activitat es corregirà presencialment a classe, mostrant la configuració aplicada als grups de seguretat i al host bastió.
