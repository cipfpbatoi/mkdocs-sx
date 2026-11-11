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
sudo apt install bind9 bind9-utils dnsutils
```

En `/etc/bind/named.conf.options` es limita la consulta i la recursió al laboratori. Si ja existeix un bloc `options`, s'edita el mateix bloc.

```bind
acl xarxa-aula { localhost; 192.168.0.0/24; };

options {
    directory "/var/cache/bind";
    allow-query { xarxa-aula; };
    allow-recursion { xarxa-aula; };
    allow-query-cache { xarxa-aula; };
    allow-transfer { none; };
    recursion yes;
    dnssec-validation auto;

    // Exemple. Es poden utilitzar els reenviadors autoritzats de l'aula.
    forwarders { 8.8.8.8; 8.8.4.4; };
};
```

## 2. Declarar les zones

En `/etc/bind/named.conf.local` es declaren la zona directa i la zona inversa privada. Per a un rang `192.168.XY.0/24`, la zona inversa serà `XY.168.192.in-addr.arpa`.

```bind
zone "nomcognom.netsx.es" {
    type primary;
    file "/etc/bind/forward.nomcognom.netsx.es";
    allow-update { none; };
};

zone "0.168.192.in-addr.arpa" {
    type primary;
    file "/etc/bind/reverse.nomcognom.netsx.es";
    allow-update { none; };
};
```

### Zona directa

Fitxer `/etc/bind/forward.nomcognom.netsx.es`.

```dns
$ORIGIN nomcognom.netsx.es.
$TTL 300
@ IN SOA dns1.nomcognom.netsx.es. hostmaster.nomcognom.netsx.es. (
    1       ; sèrie
    3600    ; refresh
    600     ; retry
    604800  ; expire
    300     ; TTL negatiu
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

Fitxer `/etc/bind/reverse.nomcognom.netsx.es`.

```dns
$ORIGIN 0.168.192.in-addr.arpa.
$TTL 300
@ IN SOA dns1.nomcognom.netsx.es. hostmaster.nomcognom.netsx.es. (
    1 3600 600 604800 300
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
sudo systemctl reload bind9
sudo systemctl status bind9 --no-pager
```

Si UFW està actiu, es permet UDP i TCP al port 53 des de la xarxa interna.

```bash
sudo ufw allow from 192.168.0.0/24 to any port 53 proto udp
sudo ufw allow from 192.168.0.0/24 to any port 53 proto tcp
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

Si falla una consulta, es revisa `sudo journalctl -u bind9 -n 50 --no-pager`. Per exemple, si BIND indica que el servidor de noms de la zona no té cap A o AAAA, cal revisar el registre de `dns1` i els punts finals. Es pot seguir la [guia de diagnòstic](fonaments/diagnostic-dns.md).

[Manual de BIND9](https://bind9.readthedocs.io/en/stable/) · [Registres i fitxers de zona](fonaments/registres-i-zones.md)
