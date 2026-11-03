---
description: Fitxers de configuració.
---

# ⚒ Fitxers de configuració.

A la pàgina de mostra del servei Apache 2 podem observar l'estructura de carpetes i fitxers de configuració del servei, tenint en compte que tots els fitxers de configuració es troben dins de la ruta /etc/apache2/

```
/etc/apache2/
|-- envvars
|-- apache2.conf
|       `--  ports.conf
|-- mods-enabled
|       |-- *.load
|       `-- *.conf
|-- conf-enabled
|       `-- *.conf
|-- sites-enabled
|       `-- *.conf
```

Entre els fitxers de configuració, podem destacar els següents:

* envvars: conté les variables del sistema utilitzades a la resta de fitxers de configuració, com ara APACHE\_RUN\_USER, o APACHE\_RUN\_GROUP, en les que estan definides l'usuari i el grup que executen el servei.&#x20;
* ports.conf: conté la configuració dels ports d'escolta del servei.
* apache2.conf: és el fitxer de configuració principal del servei, amb les directives que seran aplicades per defecte a tots els virtualhost.&#x20;
* sites-available: aquesta carpeta conté els fitxers de configuració dels virtualhost del servei (un fitxer per virtualhost), alguns dels quals poden no estar en funcionament (perquè encara estem editant-los)
* sites-enabled:  aquesta carpeta conté un enllaç simbòlic als fitxers de configuració dels virtualhost del servei que estan actius (soles crearem l'enllaç simbòlic quan vulguem activar el virtualhost corresponent).











