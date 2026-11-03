---
description: Configuració del servei SSH a Ubuntu Server 24.04
---

# ⚒️ AF.3.1.2 — Configuració del servei SSH a Ubuntu Server 24.04

Partim d'una màquina virtual, amb un sistema operatiu basat a Ubuntu Server 24.04, i que té instal·lat el servei OpenSSH-server.

* [ ] Configuració del **servidor** OpenSSH

Podem trobar la configuració del servei al fitxer /etc/ssh/**sshd\_config**, en el que podem trobar un paràmetre de configuració a cada línia del fitxer. Entre les propietats de configuració del servei, podem trobar les següents:

| Directiva                                         | Ús                                                                          |
| ------------------------------------------------- | --------------------------------------------------------------------------- |
| \`Port\`                                          | Port d'escolta del servei SSH.                                              |
| \`PermitRootLogin no\`                            | Impedix l'accés remot directe amb root.                                     |
| \`AllowUsers\` / \`AllowGroups\`                  | Restringix qui pot iniciar sessió.                                          |
| \`LoginGraceTime\`                                | Temps màxim per completar l'autenticació.                                   |
| \`MaxAuthTries\`                                  | Nombre màxim d'intents d'autenticació per connexió.                         |
| \`MaxStartups\`                                   | Limita connexions encara **no autenticades**; no limita usuaris connectats. |
| \`ClientAliveInterval\` i \`ClientAliveCountMax\` | Detecten sessions inactives.                                                |
| \`Banner\`                                        | Missatge informatiu abans de l'accés.                                       |

> **Atenció:** \`AllowHosts\`, \`DenyHosts\` i \`IdleTimeout\` no són directives d’\`sshd\_config\`. Per filtrar màquines d’origen s’ha d’emprar UFW o un tallafocs de xarxa. Abans de reiniciar, valida la sintaxi amb \`sudo sshd -t\`.

Cada volta que modifiquem la configuració del servei SSH, haurem de reiniciar el servei, i comprovar que continua funcionant correctament:

<pre class="language-bash"><code class="lang-bash"><strong>profe@sx-srv-profe-dhcp:~$ sudo service sshd restart; 
</strong>profe@sx-srv-profe-dhcp:~$ sudo service sshd status;
</code></pre>
