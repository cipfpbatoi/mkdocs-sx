---
description: Instal·lar i configurar VNC Server en LUbuntu
---

# ⚒ Instal·lar i configurar VNC Server en LUbuntu

Podem instal·lar un servidor d'escriptori remot a LUbuntu, per a poder accedir remotament a l'entorn gràfic. Existeixen múltiples alternatives, però per al nostre cas pràctic, farem servir el paquet tightvncserver.

* [ ] Instal·lació del servei:

Actualitzem el sistema:

```
profe@profe:~$ sudo apt update; sudo apt upgrade; sudo apt dist-upgrade;
```

Instal·lem l'escriptori xfce4 i el servei tightvncserver:

<pre class="language-bash"><code class="lang-bash"><strong>profe@profe:~$ sudo apt install xfce4 xfce4-goodies tightvncserver
</strong>Leyendo lista de paquetes... Hecho
Creando árbol de dependencias... Hecho
Leyendo la información de estado... Hecho
xfce4 ya está en su versión más reciente (4.16).
xfce4-goodies ya está en su versión más reciente (4.14.0).
Paquetes sugeridos:
  tightvnc-java
Se instalarán los siguientes paquetes NUEVOS:
  tightvncserver
0 actualizados, 1 nuevos se instalarán, 0 para eliminar y 1 no actualizados.
Se necesita descargar 676 kB de archivos.
Se utilizarán 1.774 kB de espacio de disco adicional después de esta operación.
¿Desea continuar? [S/n] 
</code></pre>

Obrim el port 5901, per a permetre la connexió al servei:

```
profe@profe:~$ sudo ufw allow 5901/tcp
```

I executarem el servei, per a crear els fitxers de configuració del servei, i per a configurar la contrasenya d'accés:

```bash
profe@profe:~$ vncserver

You will require a password to access your desktops.

Password: 
Verify:   
Would you like to enter a view-only password (y/n)? n

New 'X' desktop is profe:1

Creating default startup script /home/profe/.vnc/xstartup
Starting applications specified in /home/profe/.vnc/xstartup
Log file is /home/profe/.vnc/profe:1.log

```

{% hint style="info" %}
Si en algún moment volem canviar la contrasenya d'access, o crear un usuari amb permissos exclusius de visualització, podrem executar el següent comandament:

profe@profe:\~$ vncpasswd
{% endhint %}

* [ ] Configuració del servei:

Perquè tightvncserver funcione correctament amb l'escriptori xfce4 instal·lat, hem de modificar el fitxer de configuració \~/.vnc/xstartup, indicant-li quins comandaments ha d'executar quan s'inicia el servei, per tal d'executar l'entorn gràfic.&#x20;

En primer lloc, hem de detindre el servei vncserver:

```bash
profe@profe:~$ vncserver -kill :1
Killing Xtightvnc process ID 1985
```

A continuació, podem editar el fitxer \~/.vnc/xstartup, que serà executat quan iniciem el servei vncserver

```bash
#/etc/X11/Xsession
xrdb $HOME/.Xresources
startxfce4 &
```

Guardem els canvis del fitxer de configuració, i iniciem el servei vncserver:&#x20;

```bash
profe@profe:~$ vncserver;

New 'X' desktop is profe:1

Starting applications specified in /home/profe/.vnc/xstartup
Log file is /home/profe/.vnc/profe:1.log
```

Ara podrem connectar al servei d'escriptori remot, amb qualsevol client VNC, exposat al port 5901.

{% hint style="danger" %}
Cada volta que iniciem la màquina, haurem d'executar el comandament vncserver per que siga posible connectar remotament.
{% endhint %}
