---
description: IIS, instal·lat a Windows server 2022, desplegat a AWS
---

# ⚒ UD04.02.- IIS, instal·lat a Windows server 2022, desplegat a AWS

## Introducció.

Internet Information Server és un servidor web propietari de Microsoft, que ens permet allotjar llocs web, tant estàtics com dinàmics.&#x20;

## Configuració de la instància EC2.

Per a configurar el nostre servidor web IIS, haurem de:

* [Configurar un grup de seguretat internet](https://app.gitbook.com/s/dcAEDgX05ILtqXlw2HAH/pindoles-formatives/configuracio-dels-grups-de-seguretat/configuracio-del-grup-de-seguretat-internet.), que permetrà l'accés a internet de la nostra instància EC2, per a la instal·lació de paquets.
* [Configurar un grup de seguretat rdp-extern](https://app.gitbook.com/s/dcAEDgX05ILtqXlw2HAH/pindoles-formatives/configuracio-dels-grups-de-seguretat/configuracio-del-grup-de-seguretat-rdp-extern.), que permetrà l'accés RDP a la nostra instància EC2, des d'internet, per a efectuar les operacions de manteniment.
* [Configurar un grup de seguretat http-https](https://app.gitbook.com/s/dcAEDgX05ILtqXlw2HAH/pindoles-formatives/configuracio-dels-grups-de-seguretat/configuracio-del-grup-de-seguretat-http-https.), que permetrà l'accés als ports tcp/80 (http) i tcp/443 (https) a la nostra instància, per servir les webs allotjades al mateix.
* [Configurar una instància EC2](https://app.gitbook.com/s/dcAEDgX05ILtqXlw2HAH/pindoles-formatives/desplegament-duna-maquina-virtual-windows-server-2022-a-aws-academy) amb Windows Server 2022, <mark style="background-color:yellow;">**nomenada IIS**</mark>, que aplique els grups de seguretat configurats en els punts anteriors.
* Instal·lació i configuració del programari Apache 2.&#x20;

Els primers 4 punts podem fer-los seguint les instruccions dels enllaços de cada un dels paràgrafs.&#x20;

En les pàgines adients s'explicarà la instal·lació i configuració del servidor web IIS:

* [Instal·lació del servei IIS.](ud04.02.01.-instal-lacio-del-servei-iis..md)
* [Configuració de hosts virtuals.](ud04.02.02.-hosts-virtuals..md)



