---
description: Configuració del grup de seguretat 'http-https.
---

# ⚒ UDXX-02-6.- Configuració del grup de seguretat 'ftp-passiu'.

Seguint les [instruccions del tutorial d'AWS Academy](./), configurarem el grup de seguretat  'ftp-passiu', que permetrà el tràfic d'entrada del port TCP/30000 al TCP/31000 (FTP - transferència en mode passiu), des de qualsevol IP, a les instàncies que apliquen els grups de seguretat.&#x20;

Dins de la pàgina de grups de seguretat, polsem el botó "Crear nou grup de seguretat".

<figure><img src="../../.gitbook/assets/image (146).png" alt=""><figcaption><p>Llistat de grups de seguretat</p></figcaption></figure>

Introduïm les dades bàsiques del grup de seguretat 'ftp-control' (nom, descripció i VPC).

<figure><img src="../../.gitbook/assets/image (5).png" alt=""><figcaption><p>Descripció grup de seguretat FTP passiu</p></figcaption></figure>

Configurem la regla d'entrada requerida, habilitant la connexió del port TCP/30000 al port TCP/31000 (transferència de fitxers al mode passiu d'FTP) des de qualsevol IP.

<figure><img src="../../.gitbook/assets/image (6).png" alt=""><figcaption><p>Regla d'entrada FTP passiu</p></figcaption></figure>

Deixem el panell de regles d'eixida buit.

<figure><img src="../../.gitbook/assets/image (153).png" alt=""><figcaption><p>Regles d'eixida</p></figcaption></figure>

I polsem sobre el botó 'Crear grup de seguretat' per a finalitzar la configuració.&#x20;

<figure><img src="../../.gitbook/assets/image (150).png" alt=""><figcaption><p>Confirmació de la creació del grup de seguretat</p></figcaption></figure>

Tornarem al llistat de grups de seguretat, a on podrem comprovar que el grup de seguretat s'ha creat correctament.

<figure><img src="../../.gitbook/assets/image (7).png" alt=""><figcaption></figcaption></figure>
