---
description: Servei ftp, instal·lat a Windows Server 2023, desplegat a AWS.
---

# ⚒ UD05.02.- servei FTP, instal·lat a Windows Server 2023, desplegat a AWS

## Introducció.

to-do

## Configuració de la instància EC2.

Per a configurar el nostre servidor FTP, haurem de:

* [Configurar un grup de seguretat internet](https://app.gitbook.com/s/dcAEDgX05ILtqXlw2HAH/pindoles-formatives/udxx-02.-configuracio-dels-grups-de-seguretat/udxx-02-1.-configuracio-del-grup-de-seguretat-internet.), que permetrà l'accés a internet de la nostra instància EC2, per a la instal·lació de paquets.
* [Configurar un grup de seguretat rdp-extern](https://app.gitbook.com/s/dcAEDgX05ILtqXlw2HAH/pindoles-formatives/udxx-02.-configuracio-dels-grups-de-seguretat/udxx-02-3.-configuracio-del-grup-de-seguretat-rdp-extern.), que permetrà l'accés SSH a la nostra instància EC2, des d'internet, per a efectuar les operacions de manteniment.
* [Configurar un grup de seguretat ftp-control](https://app.gitbook.com/s/dcAEDgX05ILtqXlw2HAH/pindoles-formatives/udxx-02.-configuracio-dels-grups-de-seguretat/udxx-02-5.-configuracio-del-grup-de-seguretat-ftp-control), que permetrà l'accés al port TCP/21 (port de control) a la nostra instància, per a poder establir una connexió amb el nostre servidor.
* [Configurar un grup de seguretat ftp-passiu](https://app.gitbook.com/s/dcAEDgX05ILtqXlw2HAH/pindoles-formatives/udxx-02.-configuracio-dels-grups-de-seguretat/udxx-02-6.-configuracio-del-grup-de-seguretat-ftp-passiu.), que permetrà l'accés des del port TCP/30000 al TCP/31000 (ports de transferència) a la nostra instància, per a poder transmetre fitxers entre client i servidor, fent servir el mode passiu.
* [Configurar una instància EC2](https://app.gitbook.com/s/dcAEDgX05ILtqXlw2HAH/pindoles-formatives/udxx-03.-desplegament-duna-maquina-virtual-ubuntu-server-24.04-a-aws-academy) amb Windows Server 2022, <mark style="background-color:yellow;">**nomenada WINFTP**</mark>, que aplique els grups de seguretat configurats en els punts anteriors.
* Instal·lació i configuració del servei FTP.&#x20;

Els primers 5 punts podem fer-los seguint les instruccions dels enllaços de cada un dels paràgrafs.&#x20;

En les pàgines adients s'explicarà la instal·lació i configuració del servei FTP a Windows Server:

* [Instal·lació del servei FTP](ud05.02.01.-instal-lacio-del-servei..md).
* [Configuració d'accés anònim](ud05.02.02.-configuracio-dacces-anonim..md).
* [Configuració d'accés amb usuari / contrasenya.](ud05.02.03.-configuracio-dacces-nominal..md)



