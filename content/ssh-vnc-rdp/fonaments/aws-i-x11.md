# 6. SSH en AWS i aplicacions gràfiques X11

### Connexió a una instància EC2

Una instància Linux d’Amazon EC2 es pot administrar amb SSH. Abans de connectar, cal disposar de l’adreça accessible, del nom d’usuari corresponent a la imatge i d’una clau privada autoritzada.

El grup de seguretat ha de permetre l’entrada al port SSH des de l’origen previst. També han de permetre la comunicació l’encaminament, els altres controls de xarxa i el tallafocs del sistema.

Exemple per a una instància Ubuntu, substituint la destinació d’exemple per la real:

```bash
chmod 400 ~/.ssh/clau-aula.pem
ssh -i ~/.ssh/clau-aula.pem ubuntu@ec2-exemple.amazonaws.com
```

`ubuntu` és habitual en imatges Ubuntu; altres imatges utilitzen noms diferents, com `ec2-user`. El sufix `.pem` identifica un format habitual de fitxer, no una contrasenya. La clau privada s’ha de conservar en el client.

En el cas d’una instància sense IP pública, cal una via d’accés adequada, com una xarxa privada connectada o un bastió. Tindre una clau correcta no resol per si mateix la connectivitat.

La connexió també pot guardar-se en `~/.ssh/config`:

```sshconfig
Host ec2-aula
    HostName ec2-exemple.amazonaws.com
    User ubuntu
    IdentityFile ~/.ssh/clau-aula.pem
    IdentitiesOnly yes
```

### Executar una aplicació gràfica amb X11

La redirecció X11 permet executar una aplicació en el servidor i mostrar-ne la finestra en l’equip local. El procés i els fitxers de treball continuen en l’equip remot.

Cal un servidor X disponible en l’equip local, suport X11 en l’aplicació remota, `xauth` i una configuració SSH compatible. Una sessió Wayland pot oferir compatibilitat mitjançant Xwayland. En Windows o macOS sol caldre programari addicional.

En el servidor, s’ha de permetre:

```
X11Forwarding yes
```

En el client:

```bash
ssh -X alumne@192.168.0.1
```

Després es pot executar una aplicació X11 instal·lada en el servidor, com `xclock`. No s’ha de fixar `DISPLAY` manualment en una redirecció SSH normal: el client SSH el configura.

### Diferència entre -X i -Y

* `-X` sol·licita redirecció X11; la política de confiança depén també de la configuració efectiva, especialment `ForwardX11Trusted`. Amb mode no fiable s’apliquen restriccions de l’extensió X11 SECURITY.
* `-Y` sol·licita redirecció X11 **de confiança**, amb menys restriccions sobre l’accés de l’aplicació al servidor X local.

Per tant, `-Y` no és una versió «més segura» de `-X`. Atorga més confiança a l’aplicació remota. X11 forwarding mostra aplicacions; no crea necessàriament un escriptori complet i pot resultar lent amb latència elevada.

### Referències

* [AWS: connexió SSH a instàncies Linux](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connect-linux-inst-ssh.html).
* [ssh: redirecció X11](https://man.openbsd.org/ssh).
* [ssh\_config: ForwardX11 i ForwardX11Trusted](https://man.openbsd.org/ssh_config).
