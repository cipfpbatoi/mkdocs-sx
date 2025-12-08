---
description: Configuració del grup de seguretat 'http-https.
---

# ⚒ UDXX-02-5.- Configuració del grup de seguretat 'ftp-control'

Seguint les [instruccions del tutorial d'AWS Academy](./), configurarem els grups de seguretat 'ftp-control' i 'ftp-passiu', que permetrà el tràfic d'entrada al port TCP/21 (FTP - control), des de qualsevol IP, a les instàncies que apliquen els grups de seguretat.&#x20;

Dins de la pàgina de grups de seguretat, polsem el botó "Crear nou grup de seguretat".

<figure><img src="../../.gitbook/assets/image (146).png" alt=""><figcaption><p>Llistat de grups de seguretat</p></figcaption></figure>

Introduïm les dades bàsiques del grup de seguretat 'ftp-control' (nom, descripció i VPC).

<figure><img src="../../.gitbook/assets/image (1).png" alt=""><figcaption><p>Descripció del grup de seguretat</p></figcaption></figure>

Configurem la regla d'entrada requerida, habilitant la connexió al port TCP/21 (FTP) des de qualsevol IP.

<figure><img src="../../.gitbook/assets/image (2).png" alt=""><figcaption><p>Regles d'entrada</p></figcaption></figure>

Deixem el panell de regles d'eixida buit.

<figure><img src="../../.gitbook/assets/image (153).png" alt=""><figcaption><p>Regles d'eixida</p></figcaption></figure>

I polsem sobre el botó 'Crear grup de seguretat' per a finalitzar la configuració.&#x20;

<figure><img src="../../.gitbook/assets/image (150).png" alt=""><figcaption><p>Confirmació de la creació del grup de seguretat</p></figcaption></figure>

Tornarem al llistat de grups de seguretat, a on podrem comprovar que el grup de seguretat s'ha creat correctament.

<figure><img src="../../.gitbook/assets/image (3).png" alt=""><figcaption><p>Llistat de regles de seguretat</p></figcaption></figure>
