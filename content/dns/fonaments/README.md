---
icon: material/book-open-variant
description: "Fonaments del DNS: dels noms de domini a una subzona pública amb HTTPS."
---

# Fonaments del servei DNS

El **DNS (Domain Name System)** permet consultar informació associada a noms de domini. El cas més conegut és obtindre una adreça IP a partir d'un nom, però també permet localitzar servidors de correu, identificar servidors autoritatius o publicar dades de verificació.

En aquesta unitat s'estudia com es resol un nom, qui administra la informació i com es comprova si una configuració funciona. Les pràctiques comencen amb la zona personal `nomcognom.netsx.es` en VirtualBox. Primer se'n prova l'autoritat i després s'assaja la delegació des d'un pare `netsx.es` de laboratori. Amb el mateix nom, l'activitat d'AWS prepara la delegació pública del centre i la publicació d'un web amb HTTPS i un certificat de Let's Encrypt.

## Itinerari de lectura

| Capítol | Què s'ha de comprendre |
| --- | --- |
| [1. Noms, jerarquia i organització](noms-i-jerarquia.md) | Per què existeix DNS; domini, subdomini, FQDN, arrel i TLD. |
| [2. Resolució, transport i memòria cau](resolucio-i-cache.md) | Resolutors i autoritatius; recursió, iteració, UDP/TCP, TTL i respostes negatives. |
| [3. Registres i fitxers de zona](registres-i-zones.md) | SOA, NS, A, AAAA, CNAME, MX, PTR, TXT, SRV i CAA; lectura d'una zona. |
| [4. Zones, delegació i glue](delegacio-i-glue.md) | Separar responsabilitats; distingir una delegació d'un reenviament o d'una rèplica. |
| [5. El client DNS](clients-dns.md) | Resolució del sistema, fitxer hosts, Linux, Windows i DNS del navegador. |
| [6. El servidor DNS](servidors-dns.md) | BIND, zones primàries i secundàries, transferències i publicació segura. |
| [7. De netsx.es a HTTPS](netsx-es-i-https.md) | Delegació pública, IP d'AWS, verificació del domini i renovació del certificat. |
| [8. Consultes i diagnòstic](diagnostic-dns.md) | `dig`, `host`, `nslookup`, interpretació de resultats i proves des d'AWS. |
| [9. Repàs i autoavaluació](repas.md) | Relacionar conceptes i justificar els resultats de les pràctiques. |
| [Referències](referencies.md) | Materials de partida, documentació oficial i recursos complementaris. |

## Del concepte a la pràctica

Primer es treballa un DNS privat a VirtualBox. Després se separa una subzona en un altre servidor. Finalment es publica una zona delegada real en AWS. Les guies de configuració i els enunciats continuen disponibles en **Píndoles formatives** i **Pràctiques**.

Els exemples generals utilitzen `example.com`, adreces de documentació com `192.0.2.10` i adreces privades. Els exemples de `netsx.es` descriuen el domini docent del centre. **Les IP de documentació no són destinacions operatives:** en les pràctiques s'han de substituir per les IP assignades, i `nomcognom` pel nom acordat amb el professorat.

!!! warning "Atenció"

    **Proves des de la xarxa del centre.** Si una consulta DNS falla o dona un resultat inesperat, s'ha de repetir des d'una terminal de la instància Ubuntu/Linux d'AWS. La xarxa de Conselleria pot condicionar les consultes. S'han de conservar els resultats dels dos orígens i seguir el [procediment de diagnòstic](diagnostic-dns.md). Una fallada des de l'aula no demostra, per si sola, que BIND estiga mal configurat; una consulta local correcta tampoc demostra que la delegació pública funcione.


## Resultat esperat

En acabar s'ha de poder explicar una resolució completa, interpretar una resposta DNS, crear i validar una zona, justificar on van els registres de delegació, diferenciar DNS de HTTP/TLS i aportar evidències que permeten localitzar una incidència.

No és suficient que una ordre retorne «alguna IP»: cal identificar **quin servidor ha contestat, per a quin nom i tipus de registre, des de quin origen i amb quina autoritat**.
