---
icon: material/book-open-variant
description: "Materials de partida, fonts oficials i enllaços complementaris de la unitat DNS."
---

# Referències i recursos de DNS

## Materials de partida

La teoria s'ha reorganitzat a partir dels documents facilitats pel professorat:

| Document | Contingut aprofitat |
| --- | --- |
| `tema2_dns_1.pdf` | Introducció, noms i jerarquia, components, tipus de servidors, resolució, memòria cau i clients. |
| `tema2_dns_2.pdf` | Servidors, zones i registres SOA, NS, A, PTR, CNAME i MX. |
| `comandosdns.pdf` | Sintaxi, opcions i exemples de `dig`, `host` i `nslookup`. |

Els PDF són materials docents de referència facilitats a l'aula. Aquesta versió no reprodueix literalment els apunts: actualitza exemples i distingeix qüestions que podien induir a error, com el TTL negatiu del SOA, la funció dels secundaris, el paper de `systemd-resolved`, la delegació amb NS i el reenviament condicional. Les versions antigues de programari, IP i captures dels documents no s'han de copiar com a configuracions actuals.

## Documentació oficial per temes

| Tema | Font |
| --- | --- |
| Disseny i jerarquia | [RFC 1034 — Domain Names: Concepts and Facilities](https://www.rfc-editor.org/rfc/rfc1034) |
| Registres i protocol | [RFC 1035 — Domain Names: Implementation and Specification](https://www.rfc-editor.org/rfc/rfc1035) |
| Vocabulari | [RFC 9499 — DNS Terminology](https://datatracker.ietf.org/doc/html/rfc9499) |
| Memòria cau negativa | [RFC 2308](https://datatracker.ietf.org/doc/html/rfc2308) |
| TCP i DNS | [RFC 7766](https://www.rfc-editor.org/rfc/rfc7766) |
| Extensions EDNS | [RFC 6891](https://www.rfc-editor.org/rfc/rfc6891) |
| Glue en delegacions | [RFC 9471](https://www.rfc-editor.org/rfc/rfc9471.html) |
| Delegació inversa de subxarxes IPv4 | [RFC 2317](https://www.rfc-editor.org/rfc/rfc2317) |
| Transferència completa i incremental | [RFC 5936 — AXFR](https://www.rfc-editor.org/rfc/rfc5936), [RFC 1995 — IXFR](https://www.rfc-editor.org/rfc/rfc1995) |
| Notificació de canvis | [RFC 1996 — NOTIFY](https://www.rfc-editor.org/rfc/rfc1996) |
| Registres de serveis | [RFC 2782 — SRV](https://www.rfc-editor.org/rfc/rfc2782) |
| Autorització de certificació | [RFC 8659 — CAA](https://www.rfc-editor.org/rfc/rfc8659) |
| Límits de les consultes ANY | [RFC 8482](https://www.rfc-editor.org/rfc/rfc8482) |
| TLD i servidors arrel | [Base de dades d'IANA](https://www.iana.org/domains/root/db), [servidors arrel](https://www.iana.org/domains/root/servers) |
| Registre de `.es` | [Dominios.es](https://www.dominios.es/) |
| Administració BIND | [BIND Administrator Reference Manual](https://bind9.readthedocs.io/en/stable/) |
| Comandaments DNS | [Manuals de dig, host, nslookup i named-checkzone](https://bind9.readthedocs.io/en/stable/manpages.html) |
| Ubuntu Server | [Instal·lació i configuració DNS](https://ubuntu.com/server/docs/how-to/networking/install-dns/) |
| Client Linux | [systemd-resolved](https://www.freedesktop.org/software/systemd/man/latest/systemd-resolved.service.html), [Netplan](https://netplan.readthedocs.io/en/stable/netplan-yaml/) |
| Client Windows | [Resolve-DnsName](https://learn.microsoft.com/en-us/powershell/module/dnsclient/resolve-dnsname), [ipconfig](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/ipconfig) |
| IP pública i inversa en AWS | [Elastic IP](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html), [configuració de PTR](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Using_Elastic_Addressing_Reverse_DNS.html) |
| Certificats i validació de domini | [Reptes de Let's Encrypt](https://letsencrypt.org/docs/challenge-types/), [entorn de proves](https://letsencrypt.org/docs/staging-environment/) |
| Client ACME | [Guia de Certbot](https://eff-certbot.readthedocs.io/en/stable/using.html) |
| Diagnòstic HTTP/TLS | [Manual de curl](https://curl.se/docs/manpage.html) |

Els RFC fundacionals són antics i tenen actualitzacions posteriors; la capçalera de cada RFC permet consultar-les. Per a opcions i compatibilitat concretes, s'ha de contrastar la documentació amb la versió instal·lada.

## Recursos aportats pel professorat

Es conserven **tots els enllaços originals**. Comprovació orientativa efectuada l'**11 de novembre de 2026**: la consulta d'una pàgina no garanteix la reproducció d'un vídeo, el funcionament de tots els formularis ni la disponibilitat futura.

| Recurs | Enllaç original | Resultat de la comprovació i ús |
| --- | --- | --- |
| DNS a la Wikipèdia | [Domain Name System](http://es.wikipedia.org/wiki/Domain_Name_System) | Accessible amb redirecció a HTTPS. Visió general; contrastar detalls amb les fonts oficials. |
| Vídeo: Història d'Internet | [YouTube](http://www.youtube.com/watch?v=i4RE6dBAjH4) | S'ha recuperat la pàgina i el títol; reproducció no verificada. |
| Article: Com funciona DNS | [Blog de Javier Smaldone](http://blog.smaldone.com.ar/2006/12/05/como-funciona-el-dns/) | Accessible amb HTTPS. Article de 2006 útil per al funcionament conceptual; exemples històrics. |
| Vídeo: Introducció als DNS — història i funcionament | [YouTube, des de 86 s](https://www.youtube.com/watch?v=LqSqrtxrW7w&t=86s) | No s'ha pogut verificar el contingut amb la consulta automàtica. |
| Vídeo: exemple de resolució en català | [YouTube](http://www.youtube.com/watch?v=2APUdv_g1JA&feature=related) | No s'ha pogut verificar el contingut amb la consulta automàtica. |
| Vídeo: Com funciona DNS, Red.es | [YouTube](http://www.youtube.com/watch?v=dIGxJCqLJlY) | No s'ha pogut verificar el contingut amb la consulta automàtica. |
| Web Hostinger | [hostinger.es](http://www.hostinger.es) | Redirigeix a [Hostinger en castellà](https://www.hostinger.com/es). Exemple comercial de domini i allotjament. |
| Web Unelink | [unelink.es](http://www.unelink.es/) | Redirigeix a [Aire Hosting](https://hosting.airetech.es/). Exemple comercial; la marca i l'oferta han canviat. |
| Article: servidors DNS més ràpids | [ADSLZone, enllaç original](https://www.adslzone.net/internet/dns-2018) | Redirigeix a [la pàgina de DNS públics](https://www.adslzone.net/reportajes/internet/mejores-dns/). La rapidesa depén de l'origen i de les proves. |
| Web 000webhost | [000webhost.com](https://www.000webhost.com) | Es conserva com a referència històrica. Hostinger va anunciar el tancament del servei; no s'ha de plantejar com a hosting necessari per a les pràctiques. |
| Consultes DNS web | [dnsquery.org](http://dnsquery.org) | Pàgina accessible amb HTTPS; no s'ha validat cada ferramenta interactiva. |

Per al canvi de 000webhost es pot consultar l'[anunci oficial de tancament](https://www.hostinger.com/blog/000webhost-closes/). Un enllaç que no s'ha pogut comprovar no s'ha de donar automàticament per trencat.

Els proveïdors comercials són exemples per distingir registre, DNS i hosting; no cal contractar-los per completar les activitats. Les pràctiques utilitzen la infraestructura indicada pel professorat.
