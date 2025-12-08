---
description: Desplegament d'una màquina virtual Windows Server 2022 a AWS Academy
---

# ⚒ UDXX-04.- Desplegament d'una màquina virtual Windows Server 2022 a AWS Academy

En primer lloc, [accedim a la consola d'AWS](../).

<figure><img src="../.gitbook/assets/image (3) (1).png" alt=""><figcaption><p>Consola d'AWS</p></figcaption></figure>

En el buscador, introduïm les sigles 'EC2', i seleccionem l'opció 'EC2 - servidors virtuals en el núvol'.

![](<../.gitbook/assets/image (2) (1) (1).png>)&#x20;

A la pàgina d'instàncies podrem polsar sobre el link 'instancies en execució' i visualitzar el llistat d'instàncies desplegades a la nostra infraestructura al núvol d'AWS. &#x20;

<figure><img src="../.gitbook/assets/image (102).png" alt=""><figcaption><p>Opció 'instàncies en execució' del panel EC2</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (103).png" alt=""><figcaption><p>Llistat d'instàncies desplegades</p></figcaption></figure>

Per a desplegar una nova instància, haurem de polsar sobre un dels botons 'Llançar instància'.

<figure><img src="../.gitbook/assets/image (104).png" alt=""><figcaption><p>Botó llançar instància.</p></figcaption></figure>

Omplim el formulari, seguint les instruccions de l'assistent de desplegament de nova instància.&#x20;

* Introduïm el nom de la nova instància. Al nostre exemple l'anomenarem Windows server

<figure><img src="../.gitbook/assets/image (159).png" alt=""><figcaption><p>Configuració del nom de la instància</p></figcaption></figure>

* Seleccionem la imatge de sistema operatiu i aplicacions (AMI - Amazon Machine Image) que volem carregar a la nova instància. Al nostre cas, seleccionem un Windows Server 2022 base de 64 bits.

<figure><img src="../.gitbook/assets/image (160).png" alt=""><figcaption><p>Selecció d'imatge base</p></figcaption></figure>

* Seleccionem el tipus d'instància que volem desplegar, que determinarà la configuració del processador i la memòria de la instància. Al nostre cas, farem servir instàncies t2.micro, aptes per a la capa gratuïta de serveis, per tal d'abaratir els costos del nostre laboratori.

<figure><img src="../.gitbook/assets/image (107).png" alt=""><figcaption><p>Selecció de tipus d'instància.</p></figcaption></figure>

* Seleccionem el parell de claus que farem servir per a desencriptar la contrasenya d'accés RDP que farem servir per a connectar a la instància de manera remota, amb un client RDP. Podem crear un nou parell de claus o seleccionar un parell de claus prèviament generades i utilitzades a altra instància EC2.

<figure><img src="../.gitbook/assets/image (161).png" alt=""><figcaption><p>Selecció d'un parell de claus existent.</p></figcaption></figure>

* A la configuració de xarxa podem seleccionar els grups de seguretat (regles de tallafoc) que volem aplicar a la nova instància.  Aplicarem els grups de seguretat rdp-internet i internet, creats amb anterioritat, per a permetre que la instància puga accedir a internet, i nosaltres puguem connectar des d'internet a la instància per protocol RDP.

<figure><img src="../.gitbook/assets/image (162).png" alt=""><figcaption><p>Configuració dels grups de seguretat</p></figcaption></figure>

* Farem scroll fins a trobar l'opció 'Llançar instància', i el polsarem, per a aprovisionar la mateixa.&#x20;

<figure><img src="../.gitbook/assets/image (112).png" alt=""><figcaption><p>Llançar la instància</p></figcaption></figure>

Rebrem un missatge, indicant que la nova instància ha iniciat correctament, i un enllaç per poder veure totes les instàncies del nostre entorn virtual. Polsem sobre el botó 'Veure totes les instàncies'.

<figure><img src="../.gitbook/assets/image (113).png" alt=""><figcaption><p>Informació sobre la creació de la nova instància</p></figcaption></figure>

Podem observar totes les instàncies en execució, i podem seleccionar una instància, per tal de comprovar els seus paràmetres:

<figure><img src="../.gitbook/assets/image (164).png" alt=""><figcaption><p>Informació de la instància en execució</p></figcaption></figure>

Ara podem connectar per RDP a la instància EC2, amb un client RDP. Seleccionem la instància, i polsem el botó 'Connectar'.

En polsar el botó, ens mostrarà una finestra, amb la informació de connexió. Si polsem sobre l'opció 'Client RDP', podrem descarregar un fitxer de connexió amb RDP

<figure><img src="../.gitbook/assets/image (165).png" alt=""><figcaption><p>Informació de connexió a la instància</p></figcaption></figure>

Per a poder connectar amb RDP, necessitarem la contrasenya de l'usuari administrador. Per tal d'aconseguir-la, hem de polsar sobre el botó 'obtindre contrasenya' localitzat més a baix.

<figure><img src="../.gitbook/assets/image (166).png" alt=""><figcaption><p>Enllaç per a obtindre la contrasenya.</p></figcaption></figure>

En polsar l'enllaç, ens mostrarà un formulari per a importar la nostra clau privada, associada a la instància. En importar-la i polsar el botó 'Desxifrar contrasenya', ens mostrarà la contrasenya de l'administrador de la instància.&#x20;

<figure><img src="../.gitbook/assets/image (167).png" alt=""><figcaption><p>Obtenció de la contrasenya d'accés de l'administrador.</p></figcaption></figure>

Ara podem connectar amb un client d'escriptori remot que done suport al protocol RDP:

<figure><img src="../.gitbook/assets/image (168).png" alt=""><figcaption><p>Connexió amb una ferramenta d'accés a escriptori remot</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (169).png" alt=""><figcaption><p>Confirmació de la connexió</p></figcaption></figure>

Una volta connectats, podem començar a operar la instància, com si estiguérem físicament davant d'un PC amb la mateixa configuració.

<figure><img src="../.gitbook/assets/image (170).png" alt=""><figcaption><p>Pantalla de l'escriptori remot de Windows Server 2022 base</p></figcaption></figure>
