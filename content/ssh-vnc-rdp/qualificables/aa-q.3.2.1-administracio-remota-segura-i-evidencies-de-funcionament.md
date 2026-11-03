---
hidden: true
---

# AA-Q.3.2.1 — Administració remota segura i evidències de funcionament

> **Activitat d’aula qualificable única de SA03**
>
> **Tècnica d’avaluació:** activitat d’aula\
> **Instrument de qualificació:** rúbrica individual\
> **Resultat d’aprenentatge:** RA6 — Gestiona mètodes d’accés remot descrivint les seues característiques i instal·lant els servicis corresponents.

## Objectiu i condicions

Construïx i demostra l’escenari fix d’esta activitat. El treball és individual: cada evidència ha de mostrar el teu usuari o el teu identificador, encara que les màquines i la xarxa es compartisquen.

No sustituisques cap equip, protocol o recorregut per un altre sense autorització docent. No lliures contrasenyes, claus privades, fitxers `.pem`, fitxers `.ppk` ni captures que els mostren.

## Escenari obligatori

| Nom                | Sistema i rol                                                            | Configuració que has de demostrar                                                                              |
| ------------------ | ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| **GlaDOS**         | Linux amb entorn gràfic; servidor SSH i servidor VNC                     | OpenSSH reinstal·lat i VNC actiu. És el servidor Linux de les proves VNC.                                      |
| **Alyx**           | Linux amb entorn gràfic; client                                          | Client VNC i **Remmina**. Es connecta a GlaDOS per VNC i a Windows per RDP.                                    |
| **Windows**        | Windows 10/11 Pro, Education, Enterprise o Server; client i servidor RDP | Escriptori remot habilitat amb un usuari autoritzat. És el destí de Remmina i l’origen del client VNC i PuTTY. |
| **AWS-`<cognom>`** | Instància Ubuntu Server a AWS Academy                                    | Accés SSH amb clau; Webmin només accessible mitjançant túnel SSH local.                                        |

Totes les màquines locals han d’estar a la mateixa xarxa interna de VirtualBox, amb adreça IP estàtica. En la primera evidència indica les IP reals que uses; no reutilitzes les IP d’un altre alumne.

## Abans de començar: E01 — esquema i taula de connexions

Entrega un diagrama o una taula amb les quatre màquines, nom, sistema, IP, port, protocol i sentit de cada flux.

| Origen              | Destí                      | Protocol / port                 | Finalitat                               |
| ------------------- | -------------------------- | ------------------------------- | --------------------------------------- |
| Alyx                | GlaDOS                     | VNC / 5901 o el port configurat | Accés gràfic Linux → Linux              |
| Windows             | GlaDOS                     | VNC / 5901 o el port configurat | Accés gràfic Windows → Linux            |
| Alyx                | Windows                    | RDP / 3389                      | Accés gràfic Linux → Windows            |
| Windows             | AWS-`<cognom>`             | SSH / 22                        | Túnel segur i administració             |
| Windows (localhost) | AWS-`<cognom>` (localhost) | SSH -L → Webmin / 10000         | Administració web sense publicar Webmin |

## Part 1 — SSH en GlaDOS

Fes la reinstal·lació **des de la consola de VirtualBox de GlaDOS**, no des d’una sessió SSH que poguera tallar-se.

1. Desinstal·la o purga OpenSSH Server i torna’l a instal·lar.
2. Activa i inicia el servei SSH.
3. Aplica una regla UFW que permeta només el servei SSH necessari.
4. Crea o reutilitza un usuari no administrador autoritzat i configura autenticació amb clau pública.
5. Quan la clau ja funcione, aplica a `sshd_config` o a un fitxer de `sshd_config.d` estes directives: `PubkeyAuthentication yes`, `PasswordAuthentication no` i `PermitRootLogin no`.
6. Valida la sintaxi amb `sudo sshd -t` abans de recarregar o reiniciar el servei. Mantín oberta la consola de VirtualBox mentre fas la comprovació.
7. Des d’Alyx, connecta amb eixe usuari i executa una ordre remota que identifique GlaDOS. Comprova també que l’autenticació per contrasenya ja no és acceptada.

### Evidències SSH

* **E02 — Reinstal·lació:** terminal de GlaDOS amb la instal·lació completada, `systemctl status ssh` actiu i el seu nom de màquina visible.
* **E03 — Escolta, filtratge i enduriment:** resultat de `ss -tlnp` o equivalent, `ufw status verbose` i `sudo sshd -T | grep -E 'passwordauthentication|pubkeyauthentication|permitrootlogin'`. Han de veure’s el port SSH, la regla aplicada i els valors `pubkeyauthentication yes`, `passwordauthentication no` i `permitrootlogin no`.
* **E04 — Clau, bloqueig de contrasenya i registre:** des d’Alyx, connexió SSH per clau a GlaDOS i resultat de `hostnamectl` o `hostname`; mostra un intent controlat amb `ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no usuari@GlaDOS` que siga rebutjat. Afig un fragment de `journalctl -u ssh` o del registre que evidencie l’accés correcte. No mostres la clau privada.

## Part 2 — VNC: GlaDOS, Alyx i Windows

GlaDOS ha de tindre un servidor VNC funcional i protegit amb contrasenya. En xarxa d’aula, limita el tallafocs a la subxarxa interna; no exposes VNC a Internet.

1. Des d’**Alyx**, connecta a l’escriptori VNC de GlaDOS i crea la carpeta `AAQ-<cognom>` dins del directori personal de l’usuari de GlaDOS.
2. Des de **Windows**, connecta al mateix escriptori VNC de GlaDOS i crea dins de la carpeta anterior el fitxer `vnc-windows-<cognom>.txt` amb el text: `Creat des de Windows per VNC`.
3. En la consola local de **GlaDOS**, comprova que existeixen la carpeta i el fitxer i mostra el contingut.

### Evidències VNC

* **E05 — Servidor VNC:** GlaDOS mostrant nom, IP, servei o procés VNC actiu i regla de tallafocs limitada.
* **E06 — Alyx → GlaDOS:** finestra del client VNC d’Alyx amb la carpeta creada; han de veure’s origen, destinació i escriptori remot.
* **E07 — Windows → GlaDOS:** finestra del client VNC de Windows amb el fitxer creat.
* **E08 — Verificació local:** terminal o gestor de fitxers de GlaDOS mostrant `AAQ-<cognom>`, el fitxer i el seu contingut.

## Part 3 — RDP: Alyx → Windows amb Remmina

1. En **Windows**, habilita Escriptori remot, mantín NLA activat si l’edició ho permet i comprova que el tallafocs permet RDP.
2. Des d’**Alyx**, usa **Remmina** per connectar a Windows per RDP.
3. Ja dins de la sessió RDP, crea `C:\Users\Public\Documents\AAQ\rdp-<cognom>.txt` amb el text: `Creat des d'Alyx amb Remmina`.
4. Tanca la connexió i comprova localment en Windows que el fitxer continua existint i que el contingut és correcte.

### Evidències RDP

* **E09 — Windows preparat:** configuració d’Escriptori remot, usuari autoritzat i regla de tallafocs; no mostres contrasenyes.
* **E10 — Alyx → Windows:** Remmina connectat a l’escriptori Windows, amb el fitxer creat durant la sessió.
* **E11 — Verificació local:** Windows mostrant la ruta, el fitxer i el contingut després de tancar Remmina.

## Part 4 — AWS: Windows → Linux amb PuTTY, túnel SSH i Webmin

1. Crea o usa la instància **AWS-`<cognom>`**. El grup de seguretat només ha de permetre **SSH TCP/22** des de la teua IP pública actual o l’origen que determine el docent. No òbrigues 10000, VNC ni RDP.
2. Connecta des de **Windows** per SSH amb **PuTTY** i la clau autoritzada.
3. Instal·la i configura Webmin en AWS-`<cognom>` perquè el seu port 10000 no siga accessible directament des d’Internet; el servici ha d’escoltar únicament en `127.0.0.1`.
4. En PuTTY crea un túnel local: **Source port** `10000`; **Destination** `127.0.0.1:10000`; tipus **Local**.
5. Amb la sessió SSH oberta, navega des de Windows a `https://127.0.0.1:10000`.
6. En Webmin crea el grup de prova `aaq-<cognom>`. Després, en la mateixa sessió SSH de PuTTY, comprova’l amb `getent group aaq-<cognom>`.

### Evidències AWS i administració

* **E12 — Seguretat AWS:** grup de seguretat de la instància amb entrada SSH/22 restringida. Oculta IP pública, identificadors sensibles i dades de compte si cal.
* **E13 — SSH de PuTTY:** sessió Windows → AWS-`<cognom>` autenticada amb clau, amb `hostnamectl` o `hostname` visible.
* **E14 — Túnel segur:** configuració de túnels de PuTTY i comprovació al servidor que Webmin escolta en `127.0.0.1:10000`. No ha d’aparéixer una regla pública per al port 10000.
* **E15 — Acció administrativa:** Webmin obert a `https://127.0.0.1:10000`, grup `aaq-<cognom>` creat, i la verificació posterior amb `getent group` en PuTTY.

## E16 — Comparativa i incidència resolta

Inclou una taula breu, escrita amb les teues paraules, comparant SSH, RDP i VNC: xifratge, autenticació, port, ús adequat, un avantatge i una limitació de cadascun. Explica també una incidència real que hages tingut i com l’has resolta.

## Rúbrica RA6

| Criteri                                                           | Per obtindre la puntuació màxima                                                                                        | Punts |
| ----------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ----- |
| **a)** Mètodes d’accés i administració remota                     | E16 compara SSH, RDP i VNC de manera correcta i raonada.                                                                | 1     |
| **b)** Servei d’accés remot en línia de comandos                  | E02, E03 i E04 demostren reinstal·lació, tallafocs, clau pública, contrasenya deshabilitada i accés SSH segur a GlaDOS. | 1,5   |
| **c)** Servei d’accés remot en mode gràfic                        | E05–E11 demostren VNC a GlaDOS i RDP a Windows funcionals.                                                              | 1,5   |
| **d)** Comprovació dels dos mètodes                               | E04 i E06–E11 contenen connexió, acció i verificació final pròpies.                                                     | 1,5   |
| **e)** Avantatges i deficiències                                  | E16 identifica usos, avantatges i limitacions, inclosa la seguretat de VNC.                                             | 1     |
| **f)** Accés entre sistemes de diferent naturalesa                | E07 demostra Windows → Linux i E10 Linux → Windows.                                                                     | 1,5   |
| **g)** Administració remota entre sistemes de diferent naturalesa | E13–E15 demostren Windows → Linux per PuTTY, túnel SSH, Webmin i verificació de l’acció.                                | 1,5   |
| **Seguretat, documentació i autonomia**                           | E01–E16 estan identificades, ordenades, són individuals i no exposem credencials.                                       | 0,5   |

**Total: 10 punts.** Una evidència que no indique clarament número, origen, destinació i resultat no es considera vàlida fins que es complete.

## Lliurament

Entrega un únic **dossier PDF individual** amb les evidències **E01 a E16 en este ordre**. Cada evidència ha d’incloure una captura, el seu número, què demostra, màquina d’origen i màquina de destinació. No s’accepten vídeos com a lliurament.
