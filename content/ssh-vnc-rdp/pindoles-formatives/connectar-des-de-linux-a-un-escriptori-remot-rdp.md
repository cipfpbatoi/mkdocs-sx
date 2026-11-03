---
description: Connectar des de Linux a un escriptori remot RDP
---

# ⚒️ AF.3.1.11 — Connectar des de Linux a un escriptori remot RDP

Una volta hem habilitat l'acces a l'escriptori remot a un sistema Windows, amb el servei RDP, podem fer servir qualsevol client RDP per a connectar al mateix.

Al present exemple, farem servir **Remmina**, client RDP habitual en Linux.

* [ ] Descarrega i instal·lació del client.

Per a descarregar i instal·lar Remmina, fem servir l'aplicatiu apt.

```
profe@profe:~$ sudo apt install remmina;
```

* [ ] Connexió a l'escriptori remot.

Per a connectar a l'escriptori remot, obrim Remmina, i configurem la connexió, polsant sobre el botó "Connect".

<figure><img src="../assets/image (70).png" alt=""><figcaption><p>Crear nova connexió</p></figcaption></figure>

Introduïm les dades de connexió al servidor, tenint en compte que hem de seleccionar el protocol RDP:

<figure><img src="../assets/image (84).png" alt=""><figcaption></figcaption></figure>

Polsem el botó "Connect", i el client tractarà de connectar amb l'escriptori remot. Una volta s'haja establert la connexió, ens mostrarà la informació de seguretat de l'escriptori remot, i ens demanarà confirmació abans de connectar a ell.

<figure><img src="../assets/image (85).png" alt=""><figcaption><p>Informació de seguretat de l'escriptori remot</p></figcaption></figure>

Si volem continuar amb la connexió, hem de polsar el botó "Connectar", i Remmina ens demanarà la contrasenya de l'usuari:

<figure><img src="../assets/image (86).png" alt=""><figcaption><p>Autenticació d'usuari</p></figcaption></figure>

Una volta autenticat l'usuari, podem treballar amb l'escriptori remot, com si estiguérem físicament davant d'ell:

<figure><img src="../assets/image (87).png" alt=""><figcaption><p>Escriptori remot obert amb vinagre</p></figcaption></figure>
