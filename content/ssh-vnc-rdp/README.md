# FONAMENTS

L’administració remota permet gestionar un equip a través de la xarxa sense estar físicament davant d’ell: executar ordres, revisar registres, modificar configuracions o treballar amb una interfície gràfica.

Esta secció presenta els conceptes necessaris per a entendre les píndoles formatives i les pràctiques de la unitat. El fil conductor és SSH, amb una introducció a RDP i VNC.

#### Què s’ha de comprendre?

* Com es relacionen el client, el servidor, els ports i la connectivitat.
* Què aporta SSH i com es distingixen el xifratge, la identitat del servidor i l’autenticació de l’usuari.
* On es configuren el servidor i el client OpenSSH.
* Com funcionen les claus públiques, els túnels i l’agent SSH.
* Com s’apliquen estos conceptes a AWS i a l’execució d’aplicacions gràfiques.
* Quan convé utilitzar SSH, RDP o VNC.

#### Itinerari de lectura

1. [Accés remot i funcionament de SSH](fonaments/acces-remot-i-ssh.md): model client-servidor, evolució i establiment de la connexió.
2. [El servidor SSH](fonaments/servidor-ssh.md): opcions de configuració, comprovació i diagnòstic.
3. [El client SSH](fonaments/client-ssh.md): connexions, opcions i fitxer `~/.ssh/config`.
4. [Autenticació amb claus i agent SSH](fonaments/claus-i-agent-ssh.md): claus de l’usuari, permisos i delegació.
5. [Túnels i redirecció de ports](fonaments/tunels-i-redireccio-de-ports.md): redirecció local, remota i diferència respecte de NAT.
6. [SSH en AWS i aplicacions gràfiques X11](fonaments/aws-i-x11.md): connexions amb clau privada i visualització remota.
7. [Escriptori remot: RDP i VNC](fonaments/rdp-i-vnc.md): comparació, sessions i criteris de selecció.

#### Context dels exemples

Els exemples de xarxa local utilitzen un servidor accessible en `192.168.0.1` i un compte fictici `alumne`. S’han d’adaptar a la xarxa assignada, al nom d’usuari real i al port configurat. Les ordres del client s’executen a l’equip des del qual es connecta; les del servidor, a l’equip administrat.

Amb VirtualBox, el mode de xarxa determina si el servidor és accessible. Disposar d’eixida a Internet mitjançant NAT no implica que es puguen iniciar connexions cap a la màquina virtual des de qualsevol equip. Cal una xarxa accessible o una redirecció de ports adequada.

Les pàgines següents incorporen exemples i enllaços a la documentació oficial. Les píndoles formatives desenvolupen les operacions pràctiques.
