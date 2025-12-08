---
description: Teoria amb pràctica del vist a classe
---

# 💡 Introducció a DHCP

## DHCP: múltiples servidors, reenviament i renovació de concessions

### 1. Recordatori del funcionament bàsic

El **DHCP (Dynamic Host Configuration Protocol)** és un protocol de xarxa que permet assignar de manera automàtica paràmetres de configuració de xarxa als clients (IP, màscara, porta d’enllaç, DNS…).\
Funciona sobre **UDP** i utilitza dos ports:

* Port **67** per al servidor.
* Port **68** per al client.

El procés estàndard d’assignació d’una adreça es coneix com a **DORA**:

1. **Discover** → El client envia un missatge de difusió (_broadcast_) buscant servidors DHCP.
2. **Offer** → Els servidors DHCP que reben el missatge responen amb una oferta (adreça IP i paràmetres).
3. **Request** → El client tria una de les ofertes i envia una petició acceptant-la.
4. **Acknowledge** → El servidor confirma la concessió i envia definitivament la configuració al client.

Aquest procés ja el coneixeu i l’heu analitzat amb Wireshark.

***

### 2. Diversos servidors DHCP en la mateixa xarxa

En una xarxa poden existir **dos o més servidors DHCP** de manera simultània. Açò és habitual en xarxes grans (per tolerància a fallades) o en entorns mal configurats (on dos administradors han desplegat servidors sense coordinar-se).

#### Què ocorre?

* Tots els servidors reben el **DHCP Discover** del client.
* Tots responen amb un **DHCP Offer**.
* El client **no negocia ni comprova** quin és “el millor”: senzillament accepta la **primera oferta que li arriba**.
* Una vegada triada, envia el **Request** i ignora la resta.

#### Problemes que pot causar

* **Concessions duplicades** si els servidors no tenen rangs ben delimitats.
* **Clients en xarxes diferents** si cada servidor envia paràmetres incoherents (per exemple, una porta d’enllaç distinta).
* Dificultat per a fer troubleshooting, ja que els clients poden estar repartits en diferents configuracions.

#### Bones pràctiques

* **Dividir rangs d’IP** entre servidors (per exemple, un servidor gestiona .2-.100 i l’altre .101-.200).
* Configurar-los com a **servidors redundants** (failover DHCP).
* Evitar deixar dos servidors “lliures” a la mateixa LAN sense planificació.

***

### 3. Reenviament de DHCP (DHCP Relay)

El protocol DHCP es basa en missatges de difusió (_broadcast_). Açò implica que:

* El missatge de **Discover** no travessa routers.
* Per defecte, un client només pot contactar amb servidors DHCP que estiguen en la seua mateixa xarxa local.

Però, què ocorre si tenim **un únic servidor DHCP centralitzat** per a diverses xarxes?

#### DHCP Relay Agent

Un dispositiu de xarxa (generalment un router o un encaminador de nivell 3) pot actuar com a **relay agent**:

* Rep les peticions DHCP en la seua xarxa local.
* Les encapsula i les envia en **unicast** al servidor DHCP en una altra xarxa.
* Inclou informació extra, com l’**Option 82 (Relay Agent Information)**, que indica al servidor de quina xarxa prové la petició.
* El servidor respon també via relay i finalment el client rep la configuració.

#### Exemple d’escenari

```
Client (192.168.10.0/24)  --\
                             \ 
                              Router amb DHCP Relay ----> Servidor DHCP (192.168.20.10)
                             /
Client (192.168.11.0/24)  --/
```

En aquest cas, el servidor DHCP pot gestionar clients de diverses xarxes sense estar físicament en cadascuna d’elles.

***

### 4. Renovació de concessions: Renew i Rebind

Quan un client obté una IP, no la conserva indefinidament. El servidor DHCP estableix un **temps de lease (concessió)**, que pot ser de minuts, hores o dies. El client ha d’anar renovant la seua concessió seguint tres fases temporals:

1. **T1 (50% del temps de lease)**
   * El client intenta renovar l’adreça directament amb el **mateix servidor** que li la va assignar.
   * El missatge és un _DHCP Request_ enviat en **unicast**.
   * Si el servidor respon, la concessió es renova i el procés es reinicia.
2. **T2 (87,5% del temps de lease)**
   * Si el client no ha rebut resposta en T1, assumeix que el servidor original no està disponible.
   * Envia un _DHCP Request_ però en **broadcast**, per a què qualsevol servidor disponible puga contestar.
   * Açò és el que anomenem **Rebind**.
3. **Expiració (100% del lease)**
   * Si el client tampoc ha aconseguit renovar en T2, la concessió caduca.
   * El client **ja no pot utilitzar eixa IP** i ha de tornar a iniciar el procés complet **DORA**.

#### Exemple de línia temporal

Si un lease és de 8 hores:

* A les 4h → T1, el client prova un _Renew_ al servidor original.
* A les 7h → T2, el client prova un _Rebind_ amb broadcast.
* A les 8h → si no hi ha resposta, el client perd la IP i torna a _Discover_.

***

### 5. Paràmetres de configuració en un servidor DHCP

Un servidor DHCP pot configurar diversos paràmetres. Els més importants són:

* **Range d’adreces IP** → conjunt d’adreces que podrà assignar.
* **Màscara de xarxa** → defineix la grandària del segment.
* **Porta d’enllaç per defecte (router)** → adreça IP del router de sortida.
* **Servidors DNS** → adreces per a la resolució de noms.
* **Temps de lease** → duració de la concessió abans d’haver de renovar.
* **Altres opcions addicionals**:
  * Servidor WINS.
  * Domini de cerca.
  * Paràmetres per a arrencada PXE (bootp).
  * Informació de localització (Option 82, usada amb DHCP Relay).

#### Exemple de configuració bàsica (Linux, `dhcpd.conf`)

```conf
subnet 192.168.1.0 netmask 255.255.255.0 {
  range 192.168.1.100 192.168.1.200;
  option routers 192.168.1.1;
  option domain-name-servers 8.8.8.8, 1.1.1.1;
  default-lease-time 600;    # 10 minuts
  max-lease-time 7200;       # 2 hores
}
```

***

### 6. Resum de conceptes

* **Múltiples servidors DHCP** → el client tria el primer que li arriba. Cal planificar rangs i evitar conflictes.
* **DHCP Relay** → permet gestionar DHCP a través de diferents xarxes utilitzant un agent relay.
* **Renovació de leases** → T1 (Renew unicast), T2 (Rebind broadcast), Expiració (tornar a Discover).
* **Configuració mínima d’un servidor DHCP** → rang d’IP, màscara, gateway, DNS i temps de lease.
