---
description: Instal·lació del servei SSH a Ubuntu Server 24.04
---

# ⚒ Instal·lació i prova del servei SSH a Ubuntu 24.04

Partim d'una màquina virtual, amb un sistema operatiu basat a Ubuntu Server 24.04, i que té configurades tres interfícies de xarxa:

* Una connectada a NAT, perquè el servidor tinga accés a internet i puga instal·lar paquets.

<figure><img src=".gitbook/assets/image (5).png" alt=""><figcaption><p>Configuració de la interfície de xarxa de VirtualBox a NAT</p></figcaption></figure>

* Una connectada a la xarxa interna 'aula'.

<figure><img src=".gitbook/assets/image (3).png" alt=""><figcaption><p>Configuració de la interfície de xarxa de VirtualBox a Xarxa interna 'aula'</p></figcaption></figure>

* Una connectada a la xarxa 'soles anfitrio', per a poder connectar a la màquina virtual amb ssh.

<figure><img src=".gitbook/assets/image (1).png" alt=""><figcaption><p>Configuració de la interfície de xarxa de VirtualBox a Xarxa interna 'només amfitrió'</p></figcaption></figure>

Obrim un terminal, per a fer les operacions de configuració:

* [ ] Instal·lació del servei SSH&#x20;

Instal·lem el servei SSH a Ubuntu.

```bash
profe@sx-srv-profe-dhcp:~$ sudo apt install openssh-server ufw
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Suggested packages:
  molly-guard monkeysphere ssh-askpass ufw
The following NEW packages will be installed:
  openssh-server
0 upgraded, 1 newly installed, 0 to remove and 0 not upgraded.
Need to get 434 kB of archives.
After this operation, 1537 kB of additional disk space will be used.
Do you want to continue? [Y/n]
```

Recordem els comandaments per arrancar, parar, reiniciar, recarregar la configuració i consultar l'estat dels serveis SSH i UFW, així com els comandaments de reinici o recàrrega de configuració:

<pre class="language-bash"><code class="lang-bash"><strong>sudo service sshd [start|stop|restart|reload|status];
</strong>sudo service ufw [enable|disable|reload|status];
</code></pre>

També podem fer servir els comandaments corresponents, fent servir systemctl, per a activar, arrancar, parar, reiniciar, recarregar la configuració i consultar l'estat del servei:

```bash
sudo systemctl [enable|start|stop|restart|reload|status] ssh;
sudo systemctl [enable|start|stop|restart|reload|status] ufw;
```

* [ ] Habilitar la connectivitat a través del tallafocs UFW:

Per a poder connectar amb el protocol SSH al nostre servidor, hem d'obrir els ports corresponents al tallafocs del sistema. Per defecte, el servidor SSH escoltarà les peticions al port 22.

```bash
profe@sx-srv-profe-dhcp:~$ sudo ufw disable ssh
profe@sx-srv-profe-dhcp:~$ sudo ufw allow ssh
profe@sx-srv-profe-dhcp:~$ sudo ufw enable ssh
```

* [ ] Prova del servei SSH:

En instal·lar i habilitar el servei SSH, per defecte es pot accedir al sistema de manera remota amb els usuaris existents, fent servir el següent comandament:&#x20;

```
$ ssh usuari@ip_remota
```

També podem connectar sense indicar l'usuari remot. En aquest cas, es farà servir el nom de l'usuari actual a la màquina local.

```
$ ssh ip_remota
```

A la màquina virtual de prova està donat d'alta l'usuari profe, i per això podrem accedir de manera remota amb el mateix, fent servir un client SSH:

```bash
profe@clearvictus:~$ ssh profe@192.168.56.3
The authenticity of host '192.168.56.3 (192.168.56.3)' can't be established.
ECDSA key fingerprint is SHA256:hc/Sl7C03+3Empi9O5XBFtzVL2T9XVPqxtc1HI4QfkA.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

Com podem veure, la primera volta que connectem remotament amb SSH a un host remot, el client SSH ens indica que estem accedint a un nou host, i ens mostra el fingerprint del certificat que està fent servir el servidor, en el procés d'intercanvi de clau compartida, per al xifratge de la connexió de la sessió.

Per a continuar, hem d'indicar que efectivament volem connectar al host, i ens sol·licitarà la contrasenya de l'usuari, per accedir al host remot:

```bash
profe@192.168.56.3's password:
Welcome to Ubuntu 24.04.3 LTS (GNU/Linux 5.15.0-88-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Last login: Sun Nov 12 15:21:17 2023
profe@server-profe:~$
```

A partir d'aquest moment, tots els comandaments que executem, estaran executant-se al host remot, com si estiguérem teclejant-los a un teclat connectat físicament a ell (com si estiguérem treballant al davant del servidor remot).
