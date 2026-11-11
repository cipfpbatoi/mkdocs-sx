---
icon: material/hammer-wrench
description: Configuració del servei DNS a Windows Server 2022
---

# ⚒ Configuració del servei DNS a Windows Server 2022

Partim d'una màquina virtual, amb un sistema operatiu basat a Windows Server 2022, i que té configurades dues interfícies de xarxa:

* Una connectada a NAT, perquè el servidor tinga accés a internet i puga instal·lar paquets.

<figure><img src="../assets/image (3).png" alt=""><figcaption><p>Configuració de la interfície de xarxa de VirtualBox a NAT</p></figcaption></figure>

* Una connectada a la xarxa interna 'aula'.

<figure><img src="../assets/image (1).png" alt=""><figcaption><p>Configuració de la interfície de xarxa de VirtualBox a Xarxa interna 'aula'</p></figcaption></figure>

## 1. Instal·lar el rol DNS

En l'Administrador del servidor, s'obri **Administrar → Afegir rols i característiques**, se selecciona el servidor i s'instal·la el rol **Servidor DNS** amb les ferramentes d'administració. Després s'obri **Ferramentes → DNS**.

<figure><img src="../assets/image (33).png" alt="Selecció del rol DNS"><figcaption><p>Selecció del rol DNS a l'assistent.</p></figcaption></figure>

La interfície interna del servidor té IP fixa. En aquesta guia s'utilitza `192.168.0.1` en la xarxa `192.168.0.0/24`. S'adapten les IP al rang assignat. Si també s'utilitza el servidor Ubuntu, els dos exemples amb `.1` s'executen en xarxes internes separades o amb un servidor actiu cada vegada.

## 2. Crear la zona directa

En **Zones de cerca directa → Zona nova**, es crea una **zona principal** basada en fitxer, amb el nom **`nomcognom.netsx.es`**, i s'opta per no permetre actualitzacions dinàmiques. Es reemplaça `nomcognom` pel nom i primer cognom assignats, en minúscules, sense espais ni accents.

En la zona nova, s'afigen els registres **Host nou (A o AAAA)** següents, de tipus **A**:

| Nom en l'assistent | Adreça de l'exemple | Funció |
| --- | --- | --- |
| `dns1` | `192.168.0.1` | Servidor autoritatiu. |
| `gateway` | `192.168.0.1` | Porta d'enllaç, si correspon al mateix equip. |
| `intranet` | `192.168.0.200` | Servei intern. |
| `impressora` | `192.168.0.250` | Impressora de xarxa. |
| `www` | `192.168.0.200` | Nom del web que es reutilitzarà en AWS. |

En **Propietats** de la zona, s'actualitzen **SOA** i **Servidors de noms** perquè el servidor primari del SOA i el NS apunten a `dns1.nomcognom.netsx.es.`. Cal substituir el NS inicial que crea l'assistent si conté el nom local de Windows. Es comprova que l'A de `dns1` apunta a la interfície interna. En un laboratori sense secundaris, es desactiven les transferències de zona.

## 3. Crear la zona inversa i configurar els reenviadors

En **Zones de cerca inversa → Zona nova**, es crea una **zona principal IPv4**, sense actualitzacions dinàmiques, amb l'identificador de xarxa `192.168.0` per al `/24` d'exemple. S'afigen PTR per a `.1`, `.200` i `.250` amb els noms complets de `dns1`, `intranet` i `impressora`, respectivament. Si `www` i `intranet` comparteixen IP, s'utilitza `intranet` com a nom principal del PTR.

En **Propietats del servidor → Reenviadors**, es configuren els resolutors autoritzats per a consultes externes. En **Interfícies**, es limita l'escolta DNS a la IP interna del servidor. Si el tallafoc filtra les consultes de l'aula, cal permetre UDP/53 i TCP/53 des de la xarxa interna.

## 4. Comprovar des d'un client

Es configura la IP interna del servidor com a DNS del client. El sufix de cerca `nomcognom.netsx.es` és opcional. Des d'un client Windows, es pot comprovar la configuració amb `ipconfig /all` i fer aquestes proves en PowerShell:

```powershell
Resolve-DnsName nomcognom.netsx.es. -Type SOA -Server 192.168.0.1 -DnsOnly -NoRecursion
Resolve-DnsName nomcognom.netsx.es. -Type NS -Server 192.168.0.1 -DnsOnly -NoRecursion
Resolve-DnsName www.nomcognom.netsx.es. -Type A -Server 192.168.0.1 -DnsOnly -TcpOnly
nslookup 192.168.0.200 192.168.0.1
nslookup intranet.nomcognom.netsx.es.
nslookup www.iana.org.
```

Des d'un client Linux, `dig @192.168.0.1 www.nomcognom.netsx.es. A +norecurse` ha de mostrar el registre A i el senyalador `aa`. Per provar el transport TCP, es repeteix amb `+tcp`. La consulta inversa de `192.168.0.200` ha de tornar el FQDN de la intranet.

Les consultes directes funcionen amb la IP privada de VirtualBox abans de la delegació pública. La pràctica d'AWS reutilitza el nom assignat i publica els registres de servei amb les IP públiques corresponents.

[Administració de zones DNS en Windows Server](https://learn.microsoft.com/es-es/windows-server/networking/dns/manage-dns-zones) · [Guia de diagnòstic](../fonaments/diagnostic-dns.md)
