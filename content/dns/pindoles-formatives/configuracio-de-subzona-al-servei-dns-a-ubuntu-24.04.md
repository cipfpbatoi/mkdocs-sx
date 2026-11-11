---
icon: material/hammer-wrench
description: "Assaig de delegació de nomcognom.netsx.es en VirtualBox amb BIND9, NS i glue."
---

# ⚒️ Configuració de subzona al servei DNS a Ubuntu 24.04

Aquesta guia continua la [píndola de BIND9](../README.md). Es conserva la zona personal **`nomcognom.netsx.es`** i s'afegeix un segon servidor que fa de pare **`netsx.es`** dins del laboratori. S'assaja el mateix tall de zona que després configurarà el professorat en el DNS públic.

## 1. Escenari

| Equip | IP d'exemple | Paper |
| --- | --- | --- |
| DNS de l'alumne | `192.168.0.1` | Autoritatiu de `nomcognom.netsx.es`. Conserva també la zona inversa del `/24`. |
| DNS pare de proves | `192.168.0.2` | Autoritatiu de la còpia de laboratori de `netsx.es` i resolutor dels clients durant l'assaig. |
| Clients | Xarxa `192.168.0.0/24` | Consulten `192.168.0.2` per verificar la delegació. |

Es canvia `nomcognom` pel nom assignat i s'adapten les IP al rang propi. La còpia de `netsx.es` s'utilitza dins de la xarxa interna de VirtualBox. Durant l'assaig, els clients que consulten el pare local veuran la seua còpia de `netsx.es`. Per consultar la versió pública del domini cal un resolutor extern.

## 2. Preparar el servidor fill

En el primer servidor es reutilitza la zona primària de la píndola anterior. Es comprova que el SOA i l'NS fan referència a `dns1.nomcognom.netsx.es.` i que hi ha un A per a `dns1` amb la IP interna `192.168.0.1`. L'A de `www` continua apuntant al web de proves.

Per practicar també el correu, s'afigen aquests registres al fitxer de la zona filla. L'adreça d'exemple ha d'estar disponible en el rang assignat.

```dns
mail IN A  192.168.0.251
@    IN MX 10 mail.nomcognom.netsx.es.
```

S'afig el PTR corresponent a la zona inversa existent del servidor fill i s'incrementa la sèrie dels fitxers modificats.

```dns
251 IN PTR mail.nomcognom.netsx.es.
```

```bash
sudo named-checkconf
sudo named-checkzone nomcognom.netsx.es /etc/bind/forward.nomcognom.netsx.es
sudo named-checkzone 0.168.192.in-addr.arpa /etc/bind/reverse.nomcognom.netsx.es
sudo systemctl reload bind9
```

## 3. Configurar el pare de laboratori

En el segon servidor s'instal·len `bind9`, `bind9-utils` i `dnsutils`. S'apliquen les [ACL del laboratori](../README.md) per limitar consultes i recursió a la xarxa interna. Es mantenen els reenviadors generals si es necessiten per a altres dominis. La directiva `forwarders { };` en la zona del pare fa que BIND seguisca la delegació de laboratori dins de `netsx.es`.

En el bloc `options` del pare de laboratori, s'afig aquesta excepció DNSSEC perquè l'assaig utilitza una còpia local sense signar d'un domini públic. La validació continua activa per a la resta de dominis.

```bind
validate-except { "netsx.es"; };
```

En `/etc/bind/named.conf.local` es declara la zona del pare:

```bind
zone "netsx.es" {
    type primary;
    file "/etc/bind/db.netsx.es";
    allow-update { none; };
    forwarders { };
};
```

En `/etc/bind/db.netsx.es`:

```dns
$ORIGIN netsx.es.
$TTL 300
@ IN SOA ns-aula.netsx.es. hostmaster.netsx.es. (
    1 3600 600 604800 300
)
          IN NS ns-aula.netsx.es.
ns-aula   IN A  192.168.0.2

nomcognom.netsx.es.      IN NS dns1.nomcognom.netsx.es.
dns1.nomcognom.netsx.es. IN A  192.168.0.1
```

L'NS delega la zona personal. L'A que l'acompanya és el **glue** i coincideix amb l'A autoritatiu de `dns1` en el fill. El pare delega amb registres del fitxer de zona. Un reenviament condicional `type forward` només configuraria el comportament d'un resolutor concret.

```bash
sudo named-checkconf
sudo named-checkzone netsx.es /etc/bind/db.netsx.es
sudo systemctl reload bind9
```

Si hi ha tallafoc, s'autoritza UDP/53 i TCP/53 des del rang de laboratori en els dos servidors. Cal que el pare puga consultar el fill. La zona inversa es manté en un únic servidor i es prova directament contra `192.168.0.1`.

## 4. Verificar abans i després de configurar el pare

Primer es comprova l'autoritat del fill des d'un client, encara que el pare no estiga configurat:

```bash
dig @192.168.0.1 nomcognom.netsx.es. SOA +norecurse
dig @192.168.0.1 nomcognom.netsx.es. NS +norecurse
dig @192.168.0.1 www.nomcognom.netsx.es. A +norecurse
dig @192.168.0.1 www.nomcognom.netsx.es. A +tcp +norecurse
dig @192.168.0.1 -x 192.168.0.251 +norecurse
```

Es comprova que hi ha `aa` i que els registres són els esperats. Després de carregar la zona pare, es fa la consulta sense recursió abans de les consultes recursives, per observar la referència del pare amb la memòria cau buida. Si ja s'ha fet la prova recursiva, es pot buidar la cau del pare de laboratori amb `sudo rndc flush`.

```bash
# Referència del pare: NS en AUTHORITY i glue en ADDITIONAL.
dig @192.168.0.2 www.nomcognom.netsx.es. A +norecurse

# Resolució final: l'A del web i l'MX de la zona filla.
dig @192.168.0.2 www.nomcognom.netsx.es. A
dig @192.168.0.2 nomcognom.netsx.es. MX

# Amb 192.168.0.2 com a DNS del client.
dig www.nomcognom.netsx.es. A
```

`dig +trace` des de l'arrel pública es reserva per a la fase pública. L'assaig local es verifica consultant explícitament els dos servidors privats i el resolutor del client.

## 5. Reutilitzar la zona en AWS

En la [pràctica d'AWS](../practiques/aa-q.3.3.5-servidor-web-de-subzona-a-aws.md) es conserva `nomcognom.netsx.es`, el NS `dns1.nomcognom.netsx.es` i el nom `www.nomcognom.netsx.es`. Es prepara la versió pública de la zona filla amb les IP públiques dels serveis que s'han de publicar i amb la recursió pública desactivada. El professorat publica el NS i el glue en el pare públic després de rebre les evidències d'autoritat per UDP i TCP.

[Zones, delegació i glue](../fonaments/delegacio-i-glue.md) · [BIND ARM](https://bind9.readthedocs.io/en/stable/) · [RFC 9471](https://www.rfc-editor.org/rfc/rfc9471.html)
