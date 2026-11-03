# 📎 AA-Q.5.3.4 – Configuració de la seguretat bàsica HTTP amb Apache 2

#### **Objectiu de l’activitat**

Configurar mecanismes bàsics de **seguretat HTTP** en un servidor Apache2 mitjançant **autenticació d’usuaris**, aplicant-los sobre **VirtualHosts i directoris virtuals (Alias)** prèviament creats, comprovant el correcte control d’accés als diferents recursos del servidor web.

#### **Context de partida**

Es parteix de la configuració realitzada en la pràctica:

**AA-Q.5.3.2 – Configuració d’un servidor HTTP amb Apache 2**

Cal tindre configurats i funcionals els següents **VirtualHosts i directoris**, substituint _nomcognom_ pel seu **nom i primer cognom**:

***

**VirtualHost principal**

* **Domini:**\
  `nomcognom.sx`
* **DocumentRoot:**\
  `/var/www/nomcognom.sx/html/`

Aquest VirtualHost disposa dels següents **directoris virtuals (Alias)**:

* **Alias `si`**\
  _&#x52;uta real:_ `/var/www/si/html/`\
  _&#x41;ccés:_ `http://nomcognom.sx/si`
* **Alias `sox`**\
  _&#x52;uta real:_ `/var/www/sox/html/`\
  _&#x41;ccés:_ `http://nomcognom.sx/sox`
* **Alias `pw`**\
  _&#x52;uta real:_ `/var/www/pw/html/`\
  _&#x41;ccés:_ `http://nomcognom.sx/pw`

***

**VirtualHosts específics**

* **Domini:** `si.nomcognom.sx`\
  _&#x44;ocumentRoot:_ `/var/www/si/html/`
* **Domini:** `sox.nomcognom.sx`\
  _&#x44;ocumentRoot:_ `/var/www/sox/html/`
* **Domini:** `pw.nomcognom.sx`\
  _&#x44;ocumentRoot:_ `/var/www/pw/html/`

***

#### **Descripció de la tasca**

Hauràs de configurar **autenticació bàsica HTTP** en Apache2 per a restringir l’accés a determinats recursos del servidor, aplicant criteris diferents segons el **VirtualHost o directori virtual**, utilitzant **usuaris diferents per a cada recurs protegit**.

#### **Tasques a realitzar**

**1. Protecció del VirtualHost `pw.nomcognom.sx`**

* Configura el VirtualHost `pw.nomcognom.sx` perquè:
  * Tot el lloc web estiga protegit mitjançant autenticació bàsica HTTP.
  * Només els usuaris autoritzats puguen accedir al contingut.
* Crea un **usuari específic per a aquest VirtualHost**.
* Comprova:
  * Que l’accés a `http://pw.nomcognom.sx` demana usuari i contrasenya.
  * Que l’accés és correcte amb credencials vàlides.
  * Que l’accés és denegat amb credencials incorrectes.

**2. Protecció del directori virtual `pw` dins de `nomcognom.sx`**

* Protegeix únicament l’**Alias `pw`** del VirtualHost `nomcognom.sx`.
* La resta del lloc `nomcognom.sx` **no ha d’estar restringida**.
* Utilitza **un usuari diferent** del creat per al VirtualHost `pw.nomcognom.sx`.
* Verifica:
  * Que l’accés a `http://nomcognom.sx/pw` demana autenticació.
  * Que l’accés a `http://nomcognom.sx` continua sent lliure.

**3. Protecció del directori virtual `si`**

* Configura l’autenticació per al directori virtual `si`:
  * Ruta: `/var/www/si/html/`
  * Accés: `http://nomcognom.sx/si`
* Utilitza **un usuari diferent** dels anteriors.
* Comprova el correcte control d’accés.

#### **Requisits tècnics**

* L’autenticació s’ha de realitzar mitjançant **mecanismes propis d’Apache2**.
* Els fitxers de contrasenyes:
  * **No poden estar dins de cap DocumentRoot**.
* Cada recurs protegit ha de tindre:
  * Usuari propi o conjunt d’usuaris clarament diferenciats.
* El servei Apache s’ha de recarregar o reiniciar després dels canvis.

#### **Comprovacions obligatòries**

S'haurà de demostrar que:

* El servidor discrimina correctament l’accés segons:
  * VirtualHost.
  * Directori virtual.
* Els mecanismes d’autenticació funcionen de manera independent.
* Els usuaris no autoritzats no poden accedir als recursos protegits.

#### **Documentació a entregar**

S’haurà d'entregar un video de entre 3 i 4 minuts, que incloga:

* Accions de pantalla on es mostre:
  * La sol·licitud de credencials.
  * L’accés correcte als recursos protegits.
  * L’accés denegat amb credencials incorrectes.
* Fragments rellevants de configuració:
  * VirtualHost `pw.nomcognom.sx`
  * Alias `pw` i `si`
* Explicació breu de:
  * Quin recurs s’ha protegit.
  * Quin usuari s’ha associat a cada recurs.
  * Diferència entre protegir un VirtualHost i un directori virtual.

