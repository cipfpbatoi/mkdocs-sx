---
description: Connectar des de Linux a un escriptori remot VNC
---

# ⚒ Connectar des de Linux a un escriptori remot VNC

Una volta hem habilitat l'acces a l'escriptori remot a un sistema Linux, amb el servei VNC, podem fer servir qualsevol client VNC per a connectar al mateix.

Al present exemple, farem servir la versió de Linux del client vinagre.

* [ ] Descarrega i instal·lació del client.

Per a descarregar i instal·lar el client vinagre, farem servir l'aplicatiu apt.

```
profe@profe:~$ sudo apt install vinagre;
```

* [ ] Connexió a l'escriptori remot.

Per a connectar a l'escriptori remot, obrim el programari Vinagre, i configurem la connexió, pulsant sobre el botó "Connect".

<figure><img src="../.gitbook/assets/image (70).png" alt=""><figcaption><p>Crear nova connexió</p></figcaption></figure>

Introduïm les dades de connexió al servidor, tenint en compte que hem de connectar al port 5901, i polsem el botó "Connect".

<figure><img src="../.gitbook/assets/image (71).png" alt=""><figcaption><p>Configuració de les dades de connexió</p></figcaption></figure>

En connectar a l'escriptori remot, l'aplicació ens demanarà la contrasenya configurada al servei VNC.

<figure><img src="../.gitbook/assets/image (72).png" alt=""><figcaption><p>Sol·licitud de contrasenya d'accés a l'escriptori remot.</p></figcaption></figure>

Una volta introduïda la contrasenya, podrem treballar amb l'entorn gràfic, com si estiguérem físicament davant del host.

<figure><img src="../.gitbook/assets/image (73).png" alt=""><figcaption><p>Escriptori remot</p></figcaption></figure>
