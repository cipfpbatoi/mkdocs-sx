# 3. El client SSH

### Connexions bàsiques

El client inicia la connexió i selecciona l’usuari, la destinació i les opcions.

```bash
ssh alumne@192.168.0.1
ssh -p 2222 alumne@192.168.0.1
ssh alumne@192.168.0.1 hostname
```

La tercera ordre executa `hostname` al servidor i finalitza. No obri una sessió interactiva persistent.

| Opció                  | Finalitat                                |
| ---------------------- | ---------------------------------------- |
| `-p 2222`              | Port del servidor                        |
| `-i ~/.ssh/id_ed25519` | Fitxer de clau privada                   |
| `-C`                   | Sol·licita compressió                    |
| `-v`, `-vv`, `-vvv`    | Informació de diagnòstic creixent        |
| `-J usuari@bastio`     | Accés a través d’un equip intermediari   |
| `-X` / `-Y`            | Redirecció X11                           |
| `-L` / `-R`            | Redirecció local / remota                |
| `-N`                   | Connexió sense executar una ordre remota |

La compressió pot ajudar en connexions lentes amb dades compressibles. No accelera necessàriament el trànsit ja comprimit i pot afegir càrrega de CPU.

### El fitxer \~/.ssh/config

Permet definir un àlies i guardar els paràmetres de cada connexió. Es crea al compte local que executa el client.

```sshconfig
Host blackmesa
    HostName 192.168.0.1
    User alumne
    Port 22
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
    Compression no
    ServerAliveInterval 60
    ServerAliveCountMax 3
    ForwardX11 no
    ForwardAgent no
```

Després, la connexió es reduïx a:

```bash
ssh blackmesa
```

`Host` és l’àlies que s’escriu al client; `HostName` és l’adreça o el nom real. `IdentityFile` apunta a la clau privada, que continua en el client. `IdentitiesOnly yes` limita les identitats oferides a les configurades explícitament.

`ServerAliveInterval` comprova si el servidor respon a través del canal xifrat. És una opció del **client**, mentre que `ClientAliveInterval` pertany al **servidor**.

### Bastió i reutilització de connexions

`ProxyJump` permet arribar a una destinació passant per un servidor accessible:

```sshconfig
Host intern
    HostName 192.168.99.10
    User alumne
    ProxyJump blackmesa
```

Per a reutilitzar una connexió, es poden afegir estos paràmetres a una entrada `Host`:

```sshconfig
    ControlMaster auto
    ControlPath ~/.ssh/cm-%C
    ControlPersist 5m
```

La reutilització reduïx l’establiment repetit de sessions. L’àlies simplifica l’ús i evita errors; la seguretat depén de les opcions i de la protecció de les credencials.

### Referències

* [Opcions del client ssh](https://man.openbsd.org/ssh).
* [Configuració ssh\_config](https://man.openbsd.org/ssh_config).
