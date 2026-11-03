---
description: 'VirtualHost per defecte: 000-default.conf'
---

# ⚒ VirtualHost per defecte: 000-default.conf

A la carpeta /etc/apache2/sites-available/ trobarem sempre un fitxer 000-default.conf, amb la configuració del virtualhost per defecte, que escoltarà totes les peticions no associades a altes virtual host, com per exemple, les peticions realitzades directament per IP (sense nom de domini).

Al mateix, podrem observar la següent configuració:

```apacheconf
<VirtualHost *:80>
        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

* La primera línia configura un VirtualHost, que escolta peticions al port 80, des de qualsevol interfície de xarxa.
* La segona línia configura el correu electrònic de l'administrador del servei.&#x20;
* La tercera línia configura el directori en el qual hem de col·locar els documents HTML que es mostraran en accedir al VirtualHost.
* La quarta línia configura la ruta del fitxer de logs d'error.
* La quinta línia configura la ruta del fitxer de logs d'accés.
