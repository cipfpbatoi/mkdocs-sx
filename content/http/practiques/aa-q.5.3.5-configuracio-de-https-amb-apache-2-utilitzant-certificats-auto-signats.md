# 📎 AA-Q.5.3.5 – Configuració de HTTPS amb Apache 2 utilitzant certificats auto-signats

En l’activitat anterior **AA-Q.5.3.4 – Configuració de la seguretat bàsica HTTP amb Apache 2**, s’han desplegat i configurat diversos **VirtualHost** funcionant sobre **HTTP**, aplicant criteris bàsics de seguretat i organització del servei.

En aquesta nova activitat, es planteja **una evolució natural del servei**, incorporant **HTTPS** mitjançant l’ús de **certificats auto-signats**, amb l’objectiu d’assegurar les comunicacions entre client i servidor i aprofundir en la configuració avançada del servidor web.

***

### Enunciat

Una vegada desplegada una nova instància de servidor, es demana **instal·lar i configurar el servei Apache 2** de manera que **tots els llocs virtuals creats funcionen correctament sota HTTPS**, utilitzant **certificats auto-signats**, i mantenint l’estructura de dominis i hosts ja definida.

Per a aquesta activitat, **nomcognom** correspon al teu **nom i primer cognom**, i haurà de substituir-se adequadament en totes les configuracions.

***

### Requisits de configuració

#### 1. Instal·lació i preparació del servidor

* Instal·lar el servei **Apache 2** en el sistema.
* Instal·lar i habilitar els **mòduls necessaris per a HTTPS**.
* Verificar el correcte funcionament del servei abans d’aplicar HTTPS.

***

#### 2. Generació de certificats auto-signats

* Generar **certificats auto-signats** per als dominis configurats.
* Emmagatzemar correctament els certificats i claus privades.
* Utilitzar els certificats generats en la configuració dels VirtualHost HTTPS.

***

#### 3. Configuració de VirtualHost

S’hauran de configurar **els següents VirtualHost**, assegurant el seu correcte funcionament **exclusivament sota HTTPS**:

**3.1 VirtualHost principal**

* **Domini:** `nomcognom.sx`
* **DocumentRoot:**\
  `/var/www/nomcognom.sx/html/`

Aquest VirtualHost haurà de tindre configurats **els següents directoris virtuals**:

* **/si** → `/var/www/si/html/`
* **/sox** → `/var/www/sox/html/`
* **/pw** → `/var/www/pw/html/`

***

**3.2 VirtualHosts secundaris**

* **Domini:** `si.nomcognom.sx`\
  _&#x44;ocumentRoot:_ `/var/www/si/html/`
* **Domini:** `sox.nomcognom.sx`\
  _&#x44;ocumentRoot:_ `/var/www/sox/html/`
* **Domini:** `pw.nomcognom.sx`\
  _&#x44;ocumentRoot:_ `/var/www/pw/html/`

Tots aquests VirtualHost hauran de:

* Respondre correctament per **nom de domini**.
* Fer ús de **HTTPS** amb el certificat corresponent.
* No mostrar errors de configuració en el navegador (més enllà de l’avís propi dels certificats auto-signats).

***

#### 4. Seguretat i verificació

* Forçar l’ús de **HTTPS** en els VirtualHost configurats.
* Verificar que les comunicacions entre client i servidor estan xifrades.
* Comprovar l’accés als diferents dominis des del client.
* Identificar i justificar el comportament del navegador davant d’un certificat auto-signat.

***

### Documentació a entregar

S'haurá d'entregar un video de 3 a 4 minuts que incloga

* Descripció breu del funcionament de **HTTPS** i del seu paper en la seguretat web.
* Relació de mòduls d’Apache utilitzats.
* Explicació del procés de generació dels certificats auto-signats.
* Captures de pantalla que demostren:
  * Accés correcte als diferents dominis.
  * Ús de HTTPS en les connexions.
* Justificació de les decisions de configuració adoptades.

###
