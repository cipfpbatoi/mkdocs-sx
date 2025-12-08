---
description: Connectar des de Linux a un escriptori remot RDP
---

# ⚒ Connectar des de Linux a un escriptori remot RDP

Una volta hem habilitat l'acces a l'escriptori remot a un sistema Windows, amb el servei RDP, podem fer servir qualsevol client RDP per a connectar al mateix.

Al present exemple, farem servir la versió de Linux del client vinagre.

* [ ] Descarrega i instal·lació del client.

Per a descarregar i instal·lar el client vinagre, farem servir l'aplicatiu apt.

```
profe@profe:~$ sudo apt install vinagre;
```

* [ ] Connexió a l'escriptori remot.

Per a connectar a l'escriptori remot, obrim el programari Vinagre, i configurem la connexió, polsant sobre el botó "Connect".

<figure><img src="../.gitbook/assets/image (70).png" alt=""><figcaption><p>Crear nova connexió</p></figcaption></figure>

Introduïm les dades de connexió al servidor, tenint en compte que hem de seleccionar el protocol RDP:

<figure><img src="../.gitbook/assets/image (84).png" alt=""><figcaption></figcaption></figure>

Polsem el botó "Connect", i el client tractarà de connectar amb l'escriptori remot. Una volta s'haja establert la connexió, ens mostrarà la informació de seguretat de l'escriptori remot, i ens demanarà confirmació abans de connectar a ell.&#x20;

<figure><img src="../.gitbook/assets/image (85).png" alt=""><figcaption><p>Informació de seguretat de l'escriptori remot</p></figcaption></figure>

Si volem continuar amb la connexió, hem de polsar el botó "Connectar", i l'aplicatiu ens demanarà la contrasenya de l'usuari:

<figure><img src="../.gitbook/assets/image (86).png" alt=""><figcaption><p>Autenticació d'usuari</p></figcaption></figure>

Una volta autenticat l'usuari, podem treballar amb l'escriptori remot, com si estiguérem físicament davant d'ell:

<figure><img src="../.gitbook/assets/image (87).png" alt=""><figcaption><p>Escriptori remot obert amb vinagre</p></figcaption></figure>

