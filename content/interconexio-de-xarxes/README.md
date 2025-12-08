---
description: Normes de nomenclatura per a les màquines virtuals
---

# ⚒ Configuració inicial de les màquines virtuals

{% hint style="danger" %}
Les normes seran diferents depenent de l'àmbit de la màquina virtual (client/servidor) i del sistema operatiu.
{% endhint %}

## Nom de les màquines:

Farem servir la següent nomenclatura, per a designar el nom de cada màquina virtual creada, i així poder identificar correctament les màquines virtuals emprades en les configuracions de les pràctiques:

* Amb SO Linux:
  * Client: sx-cli-<mark style="color:red;">nomapellido</mark>-<mark style="color:green;">xx</mark> (exemple: sx-cli-<mark style="color:red;">jorgelopez</mark>-<mark style="color:green;">01</mark>)
  * Servidor: sx-srv-<mark style="color:red;">nomapellido</mark>-<mark style="color:green;">xx</mark> (exemple: sx-srv-<mark style="color:red;">jorgelopez</mark>-<mark style="color:green;">02</mark>)
* Amb SO windows:
  * Client: sx-wincli-<mark style="color:red;">nomapellido</mark>-<mark style="color:green;">xx</mark> (exemple: sx-wincli-<mark style="color:red;">jorgelopez</mark>-<mark style="color:green;">03</mark>)
  * Servidor: sx-winsrv-<mark style="color:red;">nomapellido</mark>-<mark style="color:green;">xx</mark> (exemple: sx-winsrv-<mark style="color:red;">jorgelopez</mark>-<mark style="color:green;">04</mark>)

En Linux, per fer efectiu el nom de la màquina, hem d'incloure el mateix al fitxer **/etc/hostname**:

```bash
sx-cli-jorgelopez-01
```

També haurem d'incloure un registre al fitxer **/etc/hosts**:

```bash
127.0.0.1 localhost sx-cli-jorgelopez-01
```

El fitxer /etc/hosts permet al sistema operatiu resoldre la IP associada a un domini, o àlies de domini, sense haver de consultar al servidor DNS.&#x20;

Aquesta funcionalitat pot ser útil durant les pràctiques, per a poder referenciar a les nostres màquines virtuals pel seu nom, sempre que estiguen configurades amb una IP fixa.&#x20;

Per eixe motiu, pot ser recomanable actualitzar els fitxers **/etc/hosts** de les màquines virtuals configurades, amb el nom i l'adreça IP de totes les màquines configurades a cada pràctica:

```bash
127.0.0.1 localhost sx-cli-jorgelopez-01

192.168.0.1 sx-srv-jorgelopez-01
192.168.0.101 sx-cli-jorgelopez-01
192.168.0.102 sx-cli-jorgelopez-02
192.168.0.103 sx-wincli-jorgelopez-01
```
