---
icon: material/hammer-wrench
description: "Zona personal nomcognom.netsx.es amb BIND9 a Ubuntu Server 24.04."
---

# ⚒️ Configuració del servei DNS a Ubuntu 24.04

Es configura la zona **`nomcognom.netsx.es`** en una màquina virtual Ubuntu Server 24.04 amb BIND9. En totes les píndoles i pràctiques, `nomcognom` es reemplaça pel nom i primer cognom assignats pel professorat, en minúscules, sense espais ni accents. Es conserva el mateix FQDN al llarg de la unitat.

## Abans de començar

Es parteix d'una màquina virtual amb Ubuntu Server 24.04 i dos adaptadors de xarxa en VirtualBox.

- Un adaptador en mode **NAT** perquè el servidor tinga eixida a Internet i puga instal·lar paquets.
- Un adaptador connectat a la **xarxa interna `aula`**, amb IP fixa. Els clients de la pràctica es connecten a la mateixa xarxa interna.

L'exemple utilitza `192.168.0.0/24` i assigna `192.168.0.1` al servidor. Si s'ha assignat un altre rang, s'adapten l'ACL, el nom de la zona inversa, les IP dels registres i les IP de les proves.

## 1. Instal·lar el servei DNS

En el servidor s'instal·len BIND9, les seues utilitats, la documentació i les eines de consulta.

```bash
sudo apt update
sudo apt install bind9 bind9-utils bind9-doc dnsutils
```

## 2. Configurar les opcions generals

S'obri el fitxer d'opcions de BIND.

```bash
sudo nano /etc/bind/named.conf.options
```

S'introdueix la configuració següent en el fitxer. L'ACL `aula-internal-network` es declara abans del bloc `options`. Si ja hi ha un bloc `options`, se substitueix pel de l'exemple.

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

- `allow-query` admet consultes del servidor mateix i dels equips de la xarxa `aula`.
- `allow-transfer` només permet les transferències de zona des de `localhost`.
- `recursion yes` activa les consultes recursives. `forwarders` indica a quins servidors es poden reenviar les consultes que BIND ha de resoldre fora de les seues zones.

Per aplicar la configuració IPv4 de la guia, també s'edita el fitxer següent.

```bash
sudo nano /etc/default/named
```

S'actualitza la línia `OPTIONS` amb el valor següent. L'opció `-4` s'aplicarà en reiniciar `named` en el pas 6.

```bash
OPTIONS="-u bind -4"
```

## 3. Declarar la zona directa i la zona inversa

S'obri el fitxer de zones locals.

```bash
sudo nano /etc/bind/named.conf.local
```

S'afigen les dues declaracions. En cada bloc s'indica que el servidor és el primari (`type master`), la ruta del fitxer de zona i que les actualitzacions dinàmiques estan desactivades.

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

La zona directa correspon a `nomcognom.netsx.es`. Per a la inversa d'una xarxa `/24`, s'escriuen al revés els tres primers octets. Per exemple, `192.168.0.0/24` correspon a `0.168.192.in-addr.arpa`.

## 4. Crear el fitxer de resolució directa

Es copia `db.local` i s'obri el fitxer nou. Es reemplaça `nomcognom` pel nom assignat també en el nom del fitxer.

```bash
sudo cp /etc/bind/db.local /etc/bind/forward.nomcognom.netsx.es
sudo nano /etc/bind/forward.nomcognom.netsx.es
```

Se substitueix tot el contingut de la plantilla pel bloc següent, amb el domini i les IP de la pràctica.

```dns
$TTL 30
@ IN SOA dns1.nomcognom.netsx.es. admin.nomcognom.netsx.es. (
    2        ; sèrie
    604800   ; refresh
    86400    ; retry
    2419200  ; expire
    604800   ; TTL negatiu
)
@          IN NS dns1.nomcognom.netsx.es.
dns1       IN A  192.168.0.1
gateway    IN A  192.168.0.1
dhcp       IN A  192.168.0.1
intranet   IN A  192.168.0.200
impressora IN A  192.168.0.250
www        IN A  192.168.0.200
```

- `$TTL 30` fixa en 30 segons el TTL per defecte dels registres de la zona.
- `@` representa la zona declarada en el pas 3. Per exemple, BIND interpreta `dns1` com a `dns1.nomcognom.netsx.es.`. El punt final dels noms complets del SOA, l'NS i els PTR indica que són absoluts.
- El `SOA` identifica el servidor primari i el contacte `admin@nomcognom.netsx.es`. La sèrie s'incrementa cada vegada que es modifica la zona. La resta de valors indiquen l'interval de refresc, el de reintent, el temps d'expiració per als secundaris i el valor que intervé en el TTL de les respostes negatives.
- L'`NS` indica quin servidor és autoritatiu per a la zona. El registre `A` de `dns1` dona l'adreça d'eixe servidor. Els altres registres `A` associen els noms dels equips i del web a les seues adreces IPv4.

## 5. Crear el fitxer de resolució inversa

Es copia `db.127` i s'obri el fitxer nou.

```bash
sudo cp /etc/bind/db.127 /etc/bind/reverse.nomcognom.netsx.es
sudo nano /etc/bind/reverse.nomcognom.netsx.es
```

Se substitueix el contingut de la plantilla pel bloc següent.

```dns
$TTL 30
@ IN SOA dns1.nomcognom.netsx.es. admin.nomcognom.netsx.es. (
    1        ; sèrie
    604800   ; refresh
    86400    ; retry
    2419200  ; expire
    604800   ; TTL negatiu
)
@   IN NS  dns1.nomcognom.netsx.es.
1   IN PTR dns1.nomcognom.netsx.es.
200 IN PTR intranet.nomcognom.netsx.es.
250 IN PTR impressora.nomcognom.netsx.es.
```

Els propietaris dels registres PTR són l'últim octet de cada IP perquè l'exemple és una xarxa `/24`. Així, `1` correspon a `192.168.0.1`, `200` a `192.168.0.200` i `250` a `192.168.0.250`. El valor del PTR és el nom complet de l'equip. Si diversos noms comparteixen una IP, en l'exemple el PTR apunta al nom principal.

## 6. Validar els fitxers i arrancar el servei

Primer es comproven la configuració general i els dos fitxers de zona.

```bash
sudo named-checkconf
sudo named-checkzone nomcognom.netsx.es /etc/bind/forward.nomcognom.netsx.es
sudo named-checkzone 0.168.192.in-addr.arpa /etc/bind/reverse.nomcognom.netsx.es
```

`named-checkconf` normalment acaba sense mostrar cap missatge si no detecta problemes. Cada `named-checkzone` ha de mostrar `OK`. Si alguna comprovació dona un error, es revisa el fitxer indicat i es repeteix la comprovació abans de continuar.

Quan les comprovacions passen, es reinicia el servei perquè llija els fitxers i aplique el mode IPv4. En consultar l'estat, s'ha de mostrar `active (running)`.

```bash
sudo systemctl enable named
sudo systemctl restart named
sudo systemctl status named --no-pager
```

## 7. Permetre les consultes al tallafoc

Si UFW està actiu, s'aplica el perfil `Bind9` i es comprova que apareix la regla. El perfil obri el port 53 per UDP i TCP. Després, BIND aplica l'ACL definida en el pas 2.

```bash
sudo ufw allow Bind9
sudo ufw status
```

## 8. Configurar el client i provar el servei

1. S'engega un client connectat a la xarxa interna `aula` i es configura `192.168.0.1` com a DNS de la interfície. Si la configuració arriba per DHCP, es modifica el DNS anunciat en el servidor DHCP i es renova la concessió del client. Per consultar noms curts, es configura `nomcognom.netsx.es` com a domini de cerca.
2. Es comprova que el client ha rebut la IP del DNS i, si s'ha configurat, el domini de cerca. En un client Linux amb NetworkManager es pot executar `nmcli device show enp0s3`, substituint `enp0s3` si la interfície té un altre nom. Amb `systemd-resolved` es pot consultar `resolvectl status`.
3. Es consulta directament BIND des del client per comprovar la resolució directa i la inversa.

    ```bash
    dig @192.168.0.1 intranet.nomcognom.netsx.es. A +norecurse
    dig @192.168.0.1 -x 192.168.0.200 +norecurse
    ```

    La primera consulta ha de retornar l'A `192.168.0.200`. La segona ha de retornar el PTR `intranet.nomcognom.netsx.es.`. Les dues respostes han de mostrar `aa`, que indica que el servidor respon com a autoritat de la zona.

4. Es comprova que el client utilitza el DNS configurat per resoldre un nom de la zona i un nom d'Internet.

    ```bash
    nslookup intranet.nomcognom.netsx.es.
    nslookup www.iana.org.
    ```

    Si s'ha configurat el domini de cerca, també es pot provar `nslookup intranet`. En un client amb `systemd-resolved`, `nslookup` pot mostrar `127.0.0.53`, que és el resolutor local. La IP del DNS que utilitza es comprova amb `resolvectl status`.

Si una consulta falla, es revisen `sudo systemctl status named` i `sudo journalctl -u named -n 50 --no-pager`. Si BIND indica que l'NS no té cap A o AAAA, es comprova que `dns1` té un registre `A` en la zona directa i que el nom complet de l'NS acaba en punt. Per a altres casos es pot seguir la [guia de diagnòstic](fonaments/diagnostic-dns.md).

## 9. Consultar el servidor des d'Internet

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
- [Manual de BIND9 sobre els fitxers de zona i l'origen implícit](https://bind9.readthedocs.io/en/v9.18.36/chapter3.html#other-zone-file-directives)
- [Registres i fitxers de zona](fonaments/registres-i-zones.md)
