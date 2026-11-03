---
icon: material/paperclip
---

# 📎 AA-Q.3.3.6 - Servidor Web de Subzona a AWS

## 1. Objectiu de la pràctica

En aquesta activitat desplegaràs una infraestructura en AWS composta per:

* Un servidor DNS autoritatiu amb una subzona pròpia.
* Un servidor web públic accessible amb un nom de domini personalitzat.
* Una delegació DNS real del domini docent `netsx.es`, gestionada pel professor.

Aquesta pràctica integra conceptes de DNS, HTTP, seguretat en xarxes i troubleshooting en entorns cloud.

## 2. Infraestructura a desplegar per alumne

Cada alumne crearà **dues instàncies EC2**, cadascuna amb una Elastic IP.

### Màquina 1 — Servidor DNS autoritatiu

* Nom canònic (FQDN): `dns1.<nomprimercognom>.netsx.es`
  * Exemple: `dns1.arturocandela.netsx.es`
* Sistema operatiu (Elegir una opció):
  * Ubuntu/Debian + Bind9
  * Windows Server + DNS Role
* Ports oberts:
  * 53/TCP i 53/UDP
  * 22/TCP (si és Linux)
  * 3389/TCP (si és Windows)

### Màquina 2 — Servidor Web

* Nom canònic (FQDN): `www.<nomprimercognom>.netsx.es`
  * Exemple: `www.arturocandela.netsx.es`
* Sistema operatiu (Elegir una opció):
  * Ubuntu/Debian + Apache2 o Nginx
  * Windows Server + IIS
* Ports oberts:
  * 80/TCP
  * 22/TCP (Linux)
  * 3389/TCP (Windows)

## 3. Security Groups a crear

Cada alumne crearà **4 Security Groups** i els aplicarà a les màquines corresponents.

### SG1 — ssh-administració

Objectiu: permetre accés remot només des de l’IP del centre.

* 22/TCP → IP pública del centre
* 3389/TCP → IP pública del centre (si s’usa Windows)
* Egress → tot permés

Aplicar a: totes les màquines.

### SG2 — eixida-internet

Objectiu: permetre connexions d’eixida.

* Ingress → cap
* Egress → 0.0.0.0/0 (tot permés)

Aplicar a: totes les màquines.

### SG3 — dns-public

Objectiu: publicar el servei DNS.

* 53/TCP → 0.0.0.0/0
* 53/UDP → 0.0.0.0/0

Aplicar a: només al servidor DNS.

### SG4 — http-public

Objectiu: publicar el web.

* 80/TCP → 0.0.0.0/0

Aplicar a: només al servidor web.

### Resum d’aplicació

* El servidor DNS utilitza: SG1, SG2 i SG3.
* El servidor Web utilitza: SG1, SG2 i SG4.

| Servidor | SG1 | SG2 | SG3 | SG4 |
| -------- | :-: | :-: | :-: | :-: |
| DNS      |  X  |  X  |  X  |     |
| WEB      |  X  |  X  |     |  X  |

## 4. Configuració de la subzona DNS

L’alumne crearà una subzona:

```
<nomprimercognom>.netsx.es
```

Exemple:

```
arturocandela.netsx.es
```

El servidor autoritatiu serà:

```
dns1.<nomprimercognom>.netsx.es
```

La zona ha d’incloure:

* SOA
* NS
* Registre A del DNS (`dns1`)
*   Registre A del web (`www`)

    ```
      ┌────────────────────────┐           ┌────────────────────────┐
      │      DNS EC2           │           │       Web EC2          │
      │ dns1.<nom>.netsx.es    │           │ www.<nom>.netsx.es     │
      ├────────────────────────┤           ├────────────────────────┤
      │ Elastic IP: X.X.X.X    │           │ Elastic IP: Y.Y.Y.Y    │
      │ SG aplicats:           │           │ SG aplicats:           │
      │  - ssh-administració   │           │  - ssh-administració   │
      │  - eixida-internet     │           │  - eixida-internet     │
      │  - dns-public          │           │  - http-public         │
      ├────────────────────────┤           ├────────────────────────┤
      │ Ports oberts:          │           │ Ports oberts:          │
      │ 53 TCP/UDP (DNS)       │           │ 80 TCP (HTTP)          │
      │ 22 SSH o 3389 RDP      │           │ 22 SSH o 3389 RDP      │
      └────────────────────────┘           └────────────────────────┘
                 │                                      │
                 │ 53 TCP/UDP                           │ 80 TCP
                 │                                      │
                 └──────────────────────┬───────────────┘
                                        │
                                        ▼
                         ┌────────────────────────┐
                         │        Internet        │
                         └────────────────────────┘
    ```

## 5. Proves obligatòries (abans de demanar la delegació)

### 5.1. Prova des del servidor DNS

```
dig @<IP_PRIVADA_DNS> www.<nomprimercognom>.netsx.es
```

### 5.2. Prova des del servidor Web

```
dig @<IP_PUBLICA_DNS> www.<nomprimercognom>.netsx.es
curl http://localhost
```

## 6. Nota sobre el firewall de capa 7 del centre

La xarxa del Conselleria utilitza un firewall de capa 7 que pot:

* Bloquejar consultes DNS directes
* Redirigir trànsit DNS
* Filtrar consultes no considerades legítimes

Per tant:

> És possible que `dig` no funcione des de l’aula encara que tot estiga ben configurat.

Això no és un error vostre.

### 6.1. Procediment si les proves des de l’aula fallen

1. Informar el professor.
2. Si el professor confirma que és problema del firewall, l’alumne crearà una **tercera instància EC2** per a proves externes.
3. Des d’eixa màquina externament es provarà:

```
dig @<IP_PUBLICA_DNS> www.<nomprimercognom>.netsx.es
curl http://<IP_PUBLICA_WEB>
```

Si funciona → la configuració és correcta.

## 7. Delegació DNS real

Quan les proves siguen correctes, el professor afegirà en el DNS de `netsx.es`:

```
<nomprimercognom>.netsx.es.      NS   dns1.<nomprimercognom>.netsx.es.
dns1.<nomprimercognom>.netsx.es. A    <IP_publica_DNS>
```

Exemple:

```
arturocandela.netsx.es.      NS   dns1.arturocandela.netsx.es.
dns1.arturocandela.netsx.es. A    54.62.123.40
```

## 8. Proves després de la delegació

Des de qualsevol lloc:

```
dig www.<nomprimercognom>.netsx.es
curl http://www.<nomprimercognom>.netsx.es
```

## 9. Contingut mínim del web

* Fitxer `index.html` amb el nom complet de l’alumne.
* Missatge de confirmació.
* Opcional: estil CSS, imatges, pàgines addicionals.

## 10. Documentació a entregar

### 10.1. Informació de configuració

* IP pública del DNS
* IP pública del Web
* Captures de configuració dels Security Groups
* Nom de la subzona

### 10.2. Proves

* Proves des del servidor DNS
* Proves des del servidor Web
* Proves des de l’aula (si funcionen)
* Proves des de la màquina externa (si s’ha necessitat)
* Proves després de la delegació

### 10.3. Configuració del DNS aportada per l’alumne

* Si s'usa Bind9:
  * \named.conf.local
  * \forward..netsx.es
* Si s'usa Windows Server - Captures de configuració de:
  * Zona
  * SOA
  * NS
  * Registres A

## 11. Criteris d’avaluació

* Funcionament del DNS autoritatiu
* Funcionament del servidor web
* Correcta configuració dels Security Groups
* Proves internes i externes realitzades
* Delegació DNS completada
* Documentació clara i completa
* Configuració DNS correcta (Bind o Windows)
* Capacitat de troubleshooting davant el firewall del centre

### 12. Activitats d'Aprofundiment

En cas d'haver acabat la pràctica, abans de l'horari establert, realitza les següents activitats (Obligatoòriament):

* [ ] Mitjançant inteligència artificial, fes una web responsive i xula utilitzant el framework de css bootstrap . La pàgina ha de ser la teua personal com si fos un currículum.
* [ ] Investiga quins registres hauries de posar per a que la direcció sense `www` també resolga el servidor web.
* [ ] Crea els registres inversos correctament per a que funcione la búsqueda inversa i afegeix-los a aws en cas de ser necessari.
* [ ] Afegeix tota la documentació al bulletí de la pràctica quan s'obriga
*
