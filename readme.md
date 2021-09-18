# WakeUp-On-Lan Python3 Script

Este script funciona em Windows e Linux.
Pensado para iniciar computadores na rede **local** utilizando Magic Packet.

## Utilização

Faça o downloas do repositório, e configure seus hosts no arquivo `wol_config.ini`, conforme o exemplo abaixo:

```
host1	192.168.2.255	a4:5e:81:f8:a9:9a
host2	192.168.2.255	7a:d8:8c:8b:c9:74
```

obs: Utilize uma linha por host, e espaços de TAB para separar as configurações.

**Executar - Windows**

Abra o terminal no diretório onde o arquivo está e digite:

> wol.py host1

ou

> python wol.py host1

**Executar - Linux**

Abra o terminal no diretório onde o arquivo está e digite:

> python3 wol.py host1

**Help**

Para obter ajuda use:

> wol.py -help

## Sobre

William Pilger | Authenty AE | Bom Principio - RS - Brasil

**Algumas Referências**

Aqui estão listadas algumas referências, nas quais foram realizadas algumas consultas.

	- [Wake-On-Lan-Python](https://github.com/bentasker/Wake-On-Lan-Python)
