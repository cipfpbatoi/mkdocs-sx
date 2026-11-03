# 7. Escriptori remot: RDP i VNC

### Accés a una interfície gràfica

Quan cal utilitzar un escriptori complet o donar assistència sobre una interfície gràfica, es pot recórrer a RDP o VNC. El client envia interaccions de teclat i ratolí i rep informació per a representar l’escriptori.

L’ordinador remot executa les aplicacions. L’equip local mostra la interfície i envia les accions de la persona usuària.

### RDP

_Remote Desktop Protocol_ és un protocol desenvolupat per Microsoft, utilitzat especialment en entorns Windows. També existixen clients per a altres sistemes i servidors com xrdp per a Linux.

Habitualment utilitza el port 3389, amb TCP i, segons el desplegament, UDP. El servidor ha de tindre habilitat el servei, autoritzar el compte i permetre l’accés de xarxa. En Windows, la possibilitat d’actuar com a servidor depén de l’edició i de la configuració.

Des d’un client Windows es pot obrir:

```
mstsc
```

Des de Linux es pot utilitzar Remmina amb el protocol RDP, indicant l’adreça i les credencials. `rdesktop` és un altre client que apareix en manuals antics; les capacitats i la compatibilitat varien entre clients.

### VNC

_Virtual Network Computing_ utilitza el protocol **RFB**, que comunica actualitzacions de la representació gràfica i esdeveniments d’entrada. Hi ha diverses implementacions, amb diferències en autenticació, xifratge i gestió de sessions.

És habitual utilitzar TCP 5900 i ports successius. La notació depén del visor: `:1` pot significar el display 1, habitualment associat al port 5901; no s’ha de confondre automàticament amb un número de port literal.

VNC pot compartir un escriptori existent o proporcionar una sessió virtual, segons el servidor utilitzat. Cal consultar la implementació concreta.

### Comparació

| Aspecte           | SSH                    | RDP                                                    | VNC                                            |
| ----------------- | ---------------------- | ------------------------------------------------------ | ---------------------------------------------- |
| Ús principal      | Ordres i administració | Escriptoris i aplicacions remotes                      | Visualització i control gràfic                 |
| Port habitual     | TCP 22                 | 3389                                                   | TCP 5900 i successius                          |
| Interfície típica | Terminal               | Gràfica                                                | Gràfica                                        |
| Protecció         | Canal SSH xifrat       | Depén de la configuració de seguretat del desplegament | Depén de la implementació i del mode           |
| Sessió            | Shell o ordre remota   | Segons sistema i servei                                | Escriptori compartit o virtual segons servidor |

No s’ha de suposar que qualsevol connexió VNC està xifrada. Es pot protegir amb mecanismes del producte, una VPN o un túnel SSH adequat. Per exemple, si VNC escolta en el port 5900 del servidor:

```bash
ssh -N -L 127.0.0.1:5901:127.0.0.1:5900 alumne@192.168.0.1
```

El visor local es connecta al port explícit 5901 de `127.0.0.1`, amb la sintaxi que requerisca. El tram SSH queda xifrat.

### Síntesi de la unitat

Cal seleccionar el protocol segons la tasca: SSH per a ordres i automatització; RDP o VNC quan es necessita interacció gràfica. En tots els casos s’han de comprovar, per este ordre, l’adreça i l’encaminament, el port i el servei, el tallafocs, la identitat i les credencials, i els permisos de la sessió.

### Referències

* [Microsoft: Remote Desktop Services](https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/overview).
* [RFB, protocol utilitzat per VNC — RFC 6143](https://www.rfc-editor.org/rfc/rfc6143).
* [TigerVNC: manual del visor i sintaxi de destinacions](https://tigervnc.org/doc/vncviewer.html).
