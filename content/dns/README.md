---
icon: material/hammer-wrench
description: "Zona personal nomcognom.netsx.es amb BIND9 a Ubuntu Server 24.04."
---

# ⚒️ Configuració del servei DNS a Ubuntu 24.04

Es configura la zona **`nomcognom.netsx.es`** en una màquina virtual Ubuntu Server 24.04 amb BIND9. En totes les píndoles i pràctiques, `nomcognom` es reemplaça pel nom i primer cognom assignats pel professorat, en minúscules, sense espais ni accents. Es conserva el mateix FQDN al llarg de la unitat.

En aquesta fase, el servidor és autoritatiu dins de VirtualBox i contesta consultes directes a la seua IP privada. La resolució des d'Internet arribarà després de la delegació pública. Per assajar-la dins de VirtualBox, es pot continuar amb la [píndola de subzona](pindoles-formatives/configuracio-de-subzona-al-servei-dns-a-ubuntu-24.04.md).

## 1. Preparar la màquina i instal·lar BIND

El servidor té una interfície en NAT per a l'eixida a Internet i una interfície amb IP fixa en la xarxa interna `aula`, compartida amb els clients. En els exemples es fa servir `192.168.0.1` en la xarxa `192.168.0.0/24`. Cal adaptar les adreces, les ACL i la zona inversa al rang assignat.

```bash
sudo apt update
sudo apt install bind9 bind9-utils bind9-doc dnsutils
```

En `/etc/bind/named.conf.options` es configura l'ACL de la xarxa interna, el reenviament i la recursió. S'edita el bloc `options` existent i es declara l'ACL fora del bloc. Si la xarxa assignada és diferent, es canvia el rang dins de l'ACL.

```bind
acl aula-internal-network {
    192.168.0.0/24;
};

options {
    directory "/var/cache/bind";
    allow-query { localhost; aula-internal-network; };
    allow-transfer { localhost; };
    forwarders {
        8.8.8.8;
        8.8.4.4;
    };
    recursion yes;
    dnssec-validation no;
    listen-on-v6 { any; };
};
```

`allow-query` permet consultes des del servidor mateix i dels equips de la xarxa de l'aula. `allow-transfer` limita les transferències de zona a `localhost`. Els reenviadors s'utilitzen per a les consultes recursives que el servidor ha d'enviar a l'exterior.

Per executar BIND en mode IPv4, es deixa la línia `OPTIONS` d'`/etc/default/named` com es mostra a continuació.

```bash
OPTIONS="-u bind -4"
```

L'opció `-4` s'aplica en reiniciar el servei. La directiva `listen-on-v6` es conserva en el fitxer d'opcions, com en la guia de referència.

## 2. Declarar les zones

En `/etc/bind/named.conf.local` es declaren la zona directa i la zona inversa privada. Per a un rang `192.168.XY.0/24`, la zona inversa serà `XY.168.192.in-addr.arpa`.

```bind
zone "nomcognom.netsx.es" IN {
    type master;
    file "/etc/bind/forward.nomcognom.netsx.es";
    allow-update { none; };
};

zone "0.168.192.in-addr.arpa" IN {
    type master;
    file "/etc/bind/reverse.nomcognom.netsx.es";
    allow-update { none; };
};
```

### Zona directa

Es pot copiar `/etc/bind/db.local` com a plantilla per al fitxer `/etc/bind/forward.nomcognom.netsx.es` i substituir-ne el contingut pel bloc següent.

```dns
$ORIGIN nomcognom.netsx.es.
$TTL 30
@ IN SOA dns1.nomcognom.netsx.es. admin.nomcognom.netsx.es. (
    2        ; sèrie
    604800   ; refresh
    86400    ; retry
    2419200  ; expire
    604800   ; TTL negatiu
)
           IN NS dns1.nomcognom.netsx.es.
dns1       IN A  192.168.0.1
gateway    IN A  192.168.0.1
dhcp       IN A  192.168.0.1
intranet   IN A  192.168.0.200
impressora IN A  192.168.0.250
www        IN A  192.168.0.200
```

`@` representa l'àpex de la zona. El punt final marca els noms absoluts. `dns1` és el nom que es farà servir per a la delegació i ha de tindre el seu propi A. S'incrementa la sèrie del SOA amb cada canvi. Si la porta d'enllaç o el servidor DHCP és un altre equip, cal adaptar-ne l'adreça. El registre `www` permet preparar el nom del web encara que el servei HTTP encara no estiga instal·lat.

### Zona inversa

Es pot copiar `/etc/bind/db.127` com a plantilla per al fitxer `/etc/bind/reverse.nomcognom.netsx.es` i substituir-ne el contingut pel bloc següent.

```dns
$ORIGIN 0.168.192.in-addr.arpa.
$TTL 30
@ IN SOA dns1.nomcognom.netsx.es. admin.nomcognom.netsx.es. (
    1 604800 86400 2419200 604800
)
    IN NS  dns1.nomcognom.netsx.es.
1   IN PTR dns1.nomcognom.netsx.es.
200 IN PTR intranet.nomcognom.netsx.es.
250 IN PTR impressora.nomcognom.netsx.es.
```

Cada PTR identifica el nom principal de l'adreça. En l'exemple, `www` i `intranet` comparteixen IP i el PTR apunta a `intranet`. Aquesta zona inversa correspon al rang privat del laboratori.

## 3. Validar i activar

```bash
sudo named-checkconf
sudo named-checkzone nomcognom.netsx.es /etc/bind/forward.nomcognom.netsx.es
sudo named-checkzone 0.168.192.in-addr.arpa /etc/bind/reverse.nomcognom.netsx.es
sudo systemctl enable named
sudo systemctl restart named
sudo systemctl status named --no-pager
```

Si UFW està actiu, s'aplica el perfil `Bind9` de la guia de referència perquè el tallafoc permeta UDP i TCP al port 53. L'ACL de BIND continua decidint quins orígens poden consultar el servei.

```bash
sudo ufw allow Bind9
sudo ufw status
```

## 4. Comprovar des d'un client

S'indica `192.168.0.1` com a DNS del client, manualment o per DHCP. El sufix de cerca `nomcognom.netsx.es` és opcional i permet consultar noms curts com `intranet`. S'utilitzen noms complets en les evidències.

```bash
dig @192.168.0.1 nomcognom.netsx.es. SOA +norecurse
dig @192.168.0.1 nomcognom.netsx.es. NS +norecurse
dig @192.168.0.1 www.nomcognom.netsx.es. A +norecurse
dig @192.168.0.1 www.nomcognom.netsx.es. A +tcp +norecurse
dig @192.168.0.1 -x 192.168.0.200 +norecurse
nslookup intranet.nomcognom.netsx.es.
nslookup www.iana.org.
```

Les consultes directes de les zones locals han de mostrar `aa`. En el cas de `www`, s'espera l'A `192.168.0.200`. La consulta inversa ha de retornar `intranet.nomcognom.netsx.es.`. Les dues últimes ordres comproven el resolutor configurat en el client, amb un nom local i un d'extern. En Ubuntu amb `systemd-resolved`, es pot comprovar el DNS de la interfície amb `resolvectl status`.

Si falla una consulta, es revisa `sudo journalctl -u named -n 50 --no-pager`. Per exemple, si BIND indica que el servidor de noms de la zona no té cap A o AAAA, cal revisar el registre de `dns1` i els punts finals. Es pot seguir la [guia de diagnòstic](fonaments/diagnostic-dns.md).

## 5. Consultar el servidor des d'Internet

L'ACL `aula-internal-network` només inclou la xarxa privada de l'aula. BIND aplica l'ACL a la IP d'origen que li arriba. Per exemple, si el client ix a Internet per NAT, es fa servir la seua IP pública d'eixida. Si es consulta a través d'un resolutor recursiu, BIND veu la IP del resolutor.

### Prova directa des d'una IP externa

En `/etc/bind/named.conf.local`, s'afig `allow-query` **dins de la zona directa**. Aquesta directiva té prioritat sobre l'`allow-query` general per a les consultes d'eixa zona. En l'exemple es reemplaça `203.0.113.25/32` per la IP d'origen que veu BIND. Es mantenen les entrades de l'aula perquè els seus clients també puguen consultar la zona.

```bind
zone "nomcognom.netsx.es" IN {
    type master;
    file "/etc/bind/forward.nomcognom.netsx.es";
    allow-update { none; };
    allow-query { localhost; aula-internal-network; 203.0.113.25/32; };
};
```

Si el mateix servidor continua resolent noms externs per als clients de l'aula durant la prova, es poden fixar `allow-recursion { localhost; aula-internal-network; };` i `allow-query-cache { localhost; aula-internal-network; };` en el bloc `options`. La IP externa només s'autoritza en la zona directa.

### Delegació pública en AWS

Per publicar la zona, es canvia l'`allow-query` **de la zona directa** per `allow-query { any; };`. Així poden consultar-la els resolutors d'Internet. En el servidor públic dedicat, es canvia `recursion yes;` per `recursion no;` en `/etc/bind/named.conf.options`. L'ACL general continua aplicant-se a la zona inversa privada si es manté en eixe servidor.

En els dos casos s'ha de permetre el port **53/UDP i 53/TCP** en el tallafoc. En AWS també s'han d'autoritzar en el Security Group del DNS. Si el servidor està darrere d'un NAT, s'han de redirigir els dos protocols fins al servidor. En una prova restringida, si s'havia aplicat una regla general `ufw allow Bind9`, se substitueix per regles per a UDP i TCP que permeten la xarxa de l'aula i l'origen de prova.

Després de validar amb `sudo named-checkconf` i aplicar el canvi amb `sudo systemctl reload named`, es fan les consultes següents des de fora. Es reemplaça `IP_PUBLICA_DNS` per la IP pública del servidor i es comprova que les dues respostes mostren `aa`.

```bash
dig @IP_PUBLICA_DNS nomcognom.netsx.es. SOA +norecurse +notcp +ignore
dig @IP_PUBLICA_DNS nomcognom.netsx.es. SOA +norecurse +tcp
```

Si BIND retorna `REFUSED` en una consulta directa a la zona carregada, es revisa la IP d'origen i l'ACL. Si la consulta expira, es comproven l'adreça, l'escolta del servei i el pas dels dos protocols pel tallafoc i el NAT.

La consulta directa per IP es pot provar abans de delegar. Per resoldre el nom amb un resolutor d'Internet, cal que el professorat publique l'NS i el glue en `netsx.es`. Els registres públics de `dns1` i `www` han de contindre les IP públiques corresponents. Es detalla en la [pràctica de subzona en AWS](practiques/aa-q.3.3.5-servidor-web-de-subzona-a-aws.md).

## Referències

- [Guia de referència de configuració DNS en Ubuntu](https://jlopezedu-informatica.gitbook.io/serveis-en-xarxa/ud02.-dns)
- [Manual de BIND9 sobre control d'accés, recursió i transferències](https://bind9.readthedocs.io/en/v9.18.33/reference.html#allow-query)
- [Registres i fitxers de zona](fonaments/registres-i-zones.md)
