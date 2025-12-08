---
description: Instal·lació del servei.
---

# ⚒ Instal·lació del servei.

Actualitzem el sistema operatiu:

```bash
ubuntu@ip-172-31-18-226:~$ sudo apt update;
ubuntu@ip-172-31-18-226:~$ sudo apt -y upgrade;
ubuntu@ip-172-31-18-226:~$ sudo apt -y dist-upgrade;
ubuntu@ip-172-31-18-226:~$ sudo apt -y autoremove;
```

Instal·lem l'aplicatiu Apache2 amb apt:

```bash
ubuntu@ip-172-31-18-226:~$ sudo apt -y install apache2;
```

Comprovem l'estat del servei

```bash
ubuntu@ip-172-31-18-226:~$ sudo systemctl status apache2
● apache2.service - The Apache HTTP Server
     Loaded: loaded (/lib/systemd/system/apache2.service; enabled; vendor pre>
     Active: active (running) since Sun 2023-12-10 13:34:47 UTC; 1h 58min ago
       Docs: https://httpd.apache.org/docs/2.4/
   Main PID: 8575 (apache2)
      Tasks: 55 (limit: 1121)
     Memory: 5.8M
        CPU: 514ms
     CGroup: /system.slice/apache2.service
             ├─8575 /usr/sbin/apache2 -k start
             ├─8577 /usr/sbin/apache2 -k start
             └─8578 /usr/sbin/apache2 -k start

```

En cas que el servei no estiga actiu, podem arrancar-lo amb els següents comandaments:

```bash
ubuntu@ip-172-31-18-226:~$ sudo systemctl enable apache2;
ubuntu@ip-172-31-18-226:~$ sudo systemctl start apache2;
```

* El primer comandament iniciarà el servei cada volta que el sistema arranque.&#x20;
* El segon comandament iniciarà el servei al moment d'executar-se.&#x20;

Comprovem l'estat d'UFW:

```bash
ubuntu@ip-172-31-18-226:~$ sudo ufw status
Status: inactive
```

En cas que UFW estiguera actiu, hem d'afegir les regles que habiliten el tràfic HTTP/HTTPS (podem afegir també les regles que habiliten el tràfic SSH, si no estigueren activades), i recarreguem la configuració d'UFW:

```
ubuntu@ip-172-31-18-226:~$ sudo ufw allow Apache
Rules updated
Rules updated (v6)
ubuntu@ip-172-31-18-226:~$ sudo ufw allow OpenSSH
Rules updated
Rules updated (v6)
ubuntu@ip-172-31-18-226:~$ sudo ufw reload;
Firewall reloaded
```

Una volta finalitzada la instal·lació, podem comprovar el funcionament, accedint al servei HTTP de la IP pública de la instància EC2, amb un navegador.&#x20;

<figure><img src="../../.gitbook/assets/image (101).png" alt=""><figcaption><p>Accés al servei HTTP instal·lat</p></figcaption></figure>



