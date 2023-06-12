# WakeUp-On-Lan Python3 Script

Este script funciona em Windows e Linux.
Pensado para iniciar computadores na rede **local** utilizando Magic Packet.

## Utilização

Faça o downloas do repositório, e configure seus hosts no arquivo `wol_config.ini`, conforme o exemplo abaixo:

```
https://sample.youdomine.com/path/to/service.php    30
```

obs: Utilize apenas uma linha. Primeiro campo é a URL, a segunda é o tempo, em segundos, de intervalo entre uma requisição e outra

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
