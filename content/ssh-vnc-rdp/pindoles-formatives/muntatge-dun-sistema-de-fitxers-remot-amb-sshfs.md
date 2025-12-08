---
description: Muntatge d'un sistema de fitxers remot amb sshfs
---

# ⚒ Muntatge d'un sistema de fitxers remot amb sshfs

Podem muntar un sistema de fitxers d'una màquina remota que exposi un servei ssh al nostre sistema de fitxers local, fent servir la ferramenta sshfs.

En primer lloc, haurem d'instal·lar la ferramenta al client:

```bash
profe@sx-srv-profe-dhcp:~$ sudo apt install sshfs
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following NEW packages will be installed:
  sshfs
0 upgraded, 1 newly installed, 0 to remove and 0 not upgraded.
Need to get 434 kB of archives.
After this operation, 1537 kB of additional disk space will be used.
Do you want to continue? [Y/n]
```

A continuació podem muntar la ruta desitjada del host remot, amb el següent comandament:

```bash
profe@clearvictus$ sshfs user@host:/remote/directory /local/directory
```

A partir d'aquest moment, qualsevol canvi realitzar al directori local serà replicat al directori remot.

Per a desmuntar la ruta, haurem d'executar el següent comandament:

```
fusermount -u /local/directory
```



