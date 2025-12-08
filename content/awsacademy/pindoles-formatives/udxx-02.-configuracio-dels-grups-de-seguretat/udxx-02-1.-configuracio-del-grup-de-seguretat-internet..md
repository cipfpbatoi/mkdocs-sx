---
description: Configuració del grup de seguretat 'internet'.
---

# ⚒ Configuració del grup de seguretat 'internet'.

Seguint les [instruccions del tutorial d'AWS Academy](./), configurarem el grup de seguretat 'internet', que permetrà el tràfic d'eixida a qualsevol IP/port, des de les instàncies que apliquen el grup de seguretat.&#x20;

Dins de la pàgina de grups de seguretat, polsem el botó "Crear nou grup de seguretat".

<figure><img src="../../.gitbook/assets/image (146).png" alt=""><figcaption><p>Llistat de grups de seguretat</p></figcaption></figure>

Introduïm les dades bàsiques del grup de seguretat 'internet' (nom, descripció i VPC).

<figure><img src="../../.gitbook/assets/image (147).png" alt=""><figcaption><p>Informació bàsica del grup de seguretat</p></figcaption></figure>

Deixem les regles d'entrada buides, perquè no volem configurar cap regla de tràfic de xarxa entrant.

<figure><img src="../../.gitbook/assets/image (148).png" alt=""><figcaption><p>Regles d'entrada</p></figcaption></figure>

Configurem la regla d'eixida, que permetrà tot el tràfic de xarxa d'eixida (permetrà la comunicació a qualsevol IP/port de destí).

<figure><img src="../../.gitbook/assets/image (149).png" alt=""><figcaption><p>Regles d'eixida</p></figcaption></figure>

I polsem sobre el botó 'Crear grup de seguretat' per a finalitzar la configuració.&#x20;

<figure><img src="../../.gitbook/assets/image (150).png" alt=""><figcaption><p>Confirmació de la creació del grup de seguretat</p></figcaption></figure>

Tornarem al llistat de grups de seguretat, a on podrem comprovar que el grup de seguretat s'ha creat correctament.













