---
icon: material/hammer-wrench
description: Publicació de www.nomcognom.netsx.es amb Apache2 i Certbot a AWS.
---

# ⚒️ Web HTTPS amb Apache2 i Certbot

Aquesta píndola publica el web **`www.nomcognom.netsx.es`** en la instància principal. El registre A de `www` ha d'apuntar a l'Elastic IP d'aquesta instància.

## 1. Abans de demanar el certificat

La delegació de `nomcognom.netsx.es` ha d'estar publicada i aquesta consulta ha de retornar l'Elastic IP correcta:

```bash
dig www.nomcognom.netsx.es. A
```

En AWS, el _Security Group_ ha de permetre **80/TCP** i **443/TCP** des d'Internet. Si UFW està actiu:

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

## 2. Instal·lar Apache2

```bash
sudo apt update
sudo apt install apache2
sudo systemctl enable --now apache2
```

Es crea el directori del lloc i una pàgina inicial:

```bash
sudo mkdir -p /var/www/www.nomcognom.netsx.es
sudo chown -R $USER:$USER /var/www/www.nomcognom.netsx.es
nano /var/www/www.nomcognom.netsx.es/index.html
```

## 3. Crear el VirtualHost HTTP

Es crea `/etc/apache2/sites-available/www.nomcognom.netsx.es.conf`:

```apache
<VirtualHost *:80>
    ServerName www.nomcognom.netsx.es
    DocumentRoot /var/www/www.nomcognom.netsx.es

    ErrorLog ${APACHE_LOG_DIR}/www.nomcognom-error.log
    CustomLog ${APACHE_LOG_DIR}/www.nomcognom-access.log combined
</VirtualHost>
```

S'activa i es valida:

```bash
sudo a2ensite www.nomcognom.netsx.es.conf
sudo a2dissite 000-default.conf
sudo apache2ctl configtest
sudo systemctl reload apache2
curl -I http://www.nomcognom.netsx.es
```

## 4. Obtenir i comprovar el certificat

Quan DNS i HTTP funcionen des d'Internet:

```bash
sudo apt install certbot python3-certbot-apache
sudo certbot --apache -d www.nomcognom.netsx.es
sudo certbot renew --dry-run
curl -I https://www.nomcognom.netsx.es
```

No s'utilitza `curl -k` com a prova de certificat vàlid. La clau privada no s'entrega mai. Si el DNS o l'HTTP no són accessibles públicament, es resol eixe problema abans de repetir la sol·licitud.

[Delegació pública i HTTPS](../fonaments/netsx-es-i-https.md) · [Diagnòstic DNS](../fonaments/diagnostic-dns.md)
