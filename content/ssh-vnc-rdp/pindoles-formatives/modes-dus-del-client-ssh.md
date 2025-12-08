---
description: Modes d'ús del client SSH
---

# ⚒ Modes d'ús del client SSH

* [ ] Establiment d'una sessió a un servei SSH remot

Com hem comentat, podem establir una sessió de treball amb un servei SSH remot, i executar comandaments al host remot.

Per a obrir una sessió de treball remot, executarem el següent comandament:

```bash
$ ssh usuari@ip_remota
```

Tenint en compte que:

* usuari és l'usuari remot amb el qual volem establir la sessió.
* ip\_remota és la IP o DNS del host amb el que volem establir la sessió.

En executar el comandament, s'establirà la connexió amb el servei SSH del host remot, i a continuació ens demanarà la contrasenya de l'usuari remot.&#x20;

A partir d'aquest moment, podrem executar comandaments al host remot.

* [ ] Execució de comandaments al host remot, sense establir una sessió SSH.

SSH ens proporciona la possibilitat d'executar un comandament al host remot, de manera segura, amb SSH, sense necessitat de mantindre la connexió oberta (s'obri la connexió, s'executa el comando especificat i es tanca la connexió).&#x20;

Per a fer-lo, hem de llançar el comandament SSH de la mateixa manera que per a establir una sessió, afegint darrere de la instrucció de connexió el comandament que volem executar, entre cometes.

La sintaxi correcta seria:

```
$ ssh profe@192.168.53.3 "ls -la";
```

* [ ] Còpia remota de fitxers

SSH ens proporciona la possibilitat de copiar fitxers d'un sistema remot, de manera segura, amb el comandament scp, especificant la ruta d'origen i destí del/s fitxers:

```
$ scp orige desti
```

Hem de tindre en compte que la ruta remota ha d'indicar-se amb el següent format:

```
user@host:/path/to/file
```

Exemples:

```
$ scp /tmp/fitxer.local profe@192.168.53.3:/home/profe/fitxer.remot
$ scp profe@192.168.53.3:/home/profe/fitxer.remot /tmp/fitxer.local 
```



