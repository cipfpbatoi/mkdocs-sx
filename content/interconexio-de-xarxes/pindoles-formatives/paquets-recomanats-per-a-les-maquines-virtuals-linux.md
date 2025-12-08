---
description: >-
  Instal·lació de paquets mínims recomanats per a fer les pràctiques en les
  màquines virtuals amb sistema operatiu Ubuntu i LUbuntu.
---

# ⚒ Paquets recomanats per a les màquines virtuals Linux

És recomanable actualitzar el sistema abans de començar:

```
sudo apt-get update;
sudo apt upgrade;
reboot;
```

Per a instal·lar VirtualBox guest additions necessitem instal·lar els paquets de compilació del kernel:

```bash
sudo apt-get install build-essential gcc make perl dkms;
reboot;
```

És interessant instal·lar el paquet net-tools, i el paquet de servidor OpenSSH-server:

```bash
sudo apt install net-tools; 
sudo apt install openssh-server;
```

Després d'instal·lar el servidor SSH, s'ha d'habilitar, per a poder accedir a la màquina de manera remota:

```bash
sudo systemctl enable ssh --now; 
sudo systemctl start ssh;
```

En cas de necessitar instal·lar el comandament ping, haurem d'instal·lar el paquet iputils-ping:

```bash
sudo apt install iputils-ping;
```
