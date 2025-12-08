---
description: Configuració del servei SSH a Ubuntu Server 24.04
---

# ⚒ Configuració del servei SSH a Ubuntu Server 24.04

Partim d'una màquina virtual, amb un sistema operatiu basat a Ubuntu Server 24.04, i que té instal·lat el servei OpenSSH-server.

* [ ] Configuració del **servidor** OpenSSH

Podem trobar la configuració del servei al fitxer /etc/ssh/**sshd\_config**, en el que podem trobar un paràmetre de configuració a cada línia del fitxer. Entre les propietats de configuració del servei, podem trobar les següents:

<table><thead><tr><th width="184">Propietat</th><th width="132">Valor inicial</th><th>Descripció</th></tr></thead><tbody><tr><td>Port</td><td>22</td><td>Port d'escolta del servei SSH</td></tr><tr><td>PermitRootLogin</td><td>no</td><td>Indica si es pot fer login amb SSH amb l'usuari root. </td></tr><tr><td>AllowUsers</td><td></td><td>Indica la llista d'usuaris que poden fer login amb SSH. (AllowUsers user1 user2)</td></tr><tr><td>DenyUsers</td><td></td><td>Indica la llista d'usuaris que NO poden fer login amb SSH. </td></tr><tr><td>LoginGraceTime</td><td></td><td>Nombre de Segons que té l'usuari remot per fer login (temps per a introduir la contrasenya)</td></tr><tr><td>MaxAuthTries</td><td></td><td>Nombre d'Intents que disposa l'usuari remot per a fer login</td></tr><tr><td>MaxStartups</td><td></td><td>Nombre màxim d'usuaris que poden estar connectats a la volta al servidor SSH</td></tr><tr><td>AllowGroups</td><td></td><td>Grups del sistema remot que poden fer login amb SSH</td></tr><tr><td>DenyGroups</td><td></td><td>Grups del sistema remot que NO poden fer login amb SSH</td></tr><tr><td>AllowHosts</td><td></td><td>Hosts des dels quals podem connectar amb SSH</td></tr><tr><td>DenyHosts</td><td></td><td>Hosts des dels quals NO podem connectar amb SSH</td></tr><tr><td>IdleTimeout</td><td></td><td>Temps en minuts/hores/dies... passats els quals el servidor força un SINGUP</td></tr><tr><td>Banner</td><td>none</td><td>Ruta del fitxer que conté un missatge ascii que es mostrarà als clients, una volta han iniciat sessió.</td></tr></tbody></table>

Cada volta que modifiquem la configuració del servei SSH, haurem de reiniciar el servei, i comprovar que continua funcionant correctament:&#x20;

<pre class="language-bash"><code class="lang-bash"><strong>profe@sx-srv-profe-dhcp:~$ sudo service sshd restart; 
</strong>profe@sx-srv-profe-dhcp:~$ sudo service sshd status;
</code></pre>

