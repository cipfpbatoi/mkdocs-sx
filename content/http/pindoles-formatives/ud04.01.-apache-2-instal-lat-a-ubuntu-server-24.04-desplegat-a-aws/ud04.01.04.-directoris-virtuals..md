---
description: Directoris virtuals.
---

# ⚒ Directoris virtuals.

Imaginem que disposem del següent fitxer de configuració de VirtualHost:

```apacheconf
<VirtualHost *:80>
        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

Tot el contingut de la nostra web hauria de copiar-se dins del directori /var/www/html/ per a poder accedir al mateix a través del navegador web.

Però potser necessitem donar accés a un directori, perquè algú puga publicar la pàgina web del seu departament, sense donar-li accés al contingut de la carpeta /var/www/html/.&#x20;

Aleshores, podríem configurar un directori virtual, per tal d'enllaçar una ruta de la nostra web amb un directori del nostre servidor.

Per exemple, quan accedim a http://34.228.160.108/sx/, que mostre el contingut de la web desplegada a /var/www/sx/html

Per a poder configurar aquest escenari, podem fer servir la directiva Alias al nostre fitxer de configuració de VirtualHost, i afegir tots els Alias que necesitem.

Per exemple, si volem afegir:

* Un Alias per a la ruta /sx, de tal manera que mostre el contingut de /var/www/sx/html/
* Un Alias per a la ruta /som, de tal manera que mostre el contingut de /var/www/som/html/
* Un Alias per a la ruta /sox, de tal manera que mostre el contingut de /var/www/sox/html/

Haurem de modificar el nostre anterior VirtualHost. Quedaria així:

```
<VirtualHost *:80>
        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html
        
        Alias "/sx" "/var/www/sx/html"
        Alias "/som" "/var/www/som/html"
        Alias "/sox" "/var/www/sox/html"
        
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

Creem l'estructura de directoris i fitxers, de tal manera que en cada ruta d'Alias tinguem un fitxer index.html, amb un element h1, que continga un text distintiu de l'alias. Quedaria una estructura similar a la següent:

```
ubuntu@ip-172-31-18-226:~$ tree /var/www/
/var/www/
├── html
│   └── index.html
├── som
│   └── html
│       └── index.html
├── sox
│   └── html
│       └── index.html
└── sx
    └── html
        └── index.html
```

Per fer efectiva la configuració, haurem de reiniciar el servei, i comprovar el seu estat:

```bash
ubuntu@ip-172-31-18-226:~$ sudo service apache2 restart
ubuntu@ip-172-31-18-226:~$ sudo service apache2 status
● apache2.service - The Apache HTTP Server
     Loaded: loaded (/lib/systemd/system/apache2.service; enabled; vendor pre>
     Active: active (running) since Sun 2023-12-10 16:58:50 UTC; 3s ago
       Docs: https://httpd.apache.org/docs/2.4/
    Process: 11111 ExecStart=/usr/sbin/apachectl start (code=exited, status=0>
   Main PID: 11117 (apache2)
      Tasks: 55 (limit: 1121)
     Memory: 4.7M
        CPU: 29ms
     CGroup: /system.slice/apache2.service
             ├─11117 /usr/sbin/apache2 -k start
             ├─11118 /usr/sbin/apache2 -k start
             └─11119 /usr/sbin/apache2 -k start

Dec 10 16:58:50 ip-172-31-18-226 systemd[1]: Starting The Apache HTTP Server.>
Dec 10 16:58:50 ip-172-31-18-226 systemd[1]: Started The Apache HTTP Server.
lines 1-16/16 (END)

```

I podem accedir a les rutes configurades.&#x20;

<figure><img src="../../.gitbook/assets/image (102).png" alt=""><figcaption><p>Prova d'accés a un directori virtual.</p></figcaption></figure>



