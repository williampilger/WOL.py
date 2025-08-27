# Sistema WOL - Wake on LAN

Sistema completo para controle e monitoramento de PCs na rede local, com funcionalidades de Wake-on-LAN, monitoramento de status e gerenciamento de usuários e grupos.

## 🚀 Características

### Funcionalidades Principais
- **Wake-on-LAN (WOL)**: Ligar dispositivos remotamente
- **Monitoramento de Status**: Verificação automática de dispositivos online/offline
- **Scan de Rede**: Descoberta automática de dispositivos na rede
- **Interface Web**: Acesso via navegador responsivo
- **Controle de Usuários**: Sistema de autenticação e permissões
- **Grupos de Dispositivos**: Organização e controle de acesso por grupos
- **Logs de Atividade**: Histórico completo de ações realizadas

### Tecnologias Utilizadas
- **Backend**: Python 3.11, Flask, SQLAlchemy
- **Frontend**: Bootstrap 5, HTML5, JavaScript
- **Banco de Dados**: SQLite (integrado)
- **Containerização**: Docker, Docker Compose
- **Bibliotecas de Rede**: python-nmap, ping3, wakeonlan

## 📋 Requisitos

### Requisitos do Sistema
- Docker e Docker Compose instalados
- Acesso à rede local onde estão os dispositivos
- Porta disponível para o serviço web (padrão: 5000)

### Requisitos dos Dispositivos de Destino
- Wake-on-LAN habilitado na BIOS/UEFI
- Placa de rede configurada para "Wake on Magic Packet"
- Conexão via cabo de rede (recomendado)

## 🛠️ Instalação e Configuração

### 1. Clone do Repositório
```bash
git clone <seu-repositorio>
cd web_wol_client
```

### 2. Configuração do Docker Compose
Edite o arquivo `docker-compose.yml` se necessário para alterar a porta:

```yaml
ports:
  - "5000:5000"  # Altere a primeira porta conforme necessário
```

### 3. Inicialização do Sistema
```bash
# Construir e iniciar o container
docker-compose up -d

# Verificar logs
docker-compose logs -f
```

### 4. Primeiro Acesso
1. Acesse `http://localhost:5000` (ou IP do servidor + porta configurada)
2. Faça login com as credenciais padrão:
   - **Usuário**: `admin`
   - **Senha**: `admin123`
3. **IMPORTANTE**: Altere a senha padrão imediatamente!

## 📖 Guia de Uso

### Configuração Inicial

#### 1. Alterar Senha do Administrador
- Acesse o menu do usuário → "Alterar Senha"
- Digite a senha atual (`admin123`) e defina uma nova senha segura

#### 2. Criar Grupos de Dispositivos
- Vá para "Administração" → "Grupos"
- Clique em "Adicionar Grupo"
- Defina nome e descrição do grupo

#### 3. Adicionar Dispositivos
- Vá para "Dispositivos" → "Adicionar Dispositivo"
- Preencha as informações necessárias:
  - **Nome**: Nome identificador do dispositivo
  - **IP**: Endereço IP fixo do dispositivo
  - **MAC**: Endereço MAC da placa de rede
  - **Grupos**: Selecione os grupos apropriados

### Operações Principais

#### Wake-on-LAN
1. Acesse "Wake on LAN" no menu
2. Selecione os dispositivos desejados
3. Clique em "Enviar Wake-on-LAN"
4. Verifique os resultados nas mensagens de retorno

#### Monitoramento
- O sistema monitora automaticamente os dispositivos configurados
- Status é atualizado via ping periódico
- Visualize o status no Dashboard ou na lista de Dispositivos

#### Scan de Rede
- Acesse "Administração" → "Scan de Rede"
- Configure a faixa de rede (ex: `192.168.1.0/24`)
- Execute o scan para descobrir dispositivos ativos

### Gerenciamento de Usuários

#### Criar Usuário
1. Acesse "Administração" → "Usuários"
2. Clique em "Adicionar Usuário"
3. Configure as permissões e grupos de acesso

#### Controle de Acesso
- **Administradores**: Acesso total ao sistema
- **Usuários normais**: Acesso apenas aos dispositivos de seus grupos
- Usuários podem ser ativados/desativados

## 🔧 Configurações Avançadas

### Variáveis de Ambiente
Crie um arquivo `.env` para personalizar configurações:

```bash
# Porta do serviço
FLASK_PORT=5000

# Caminho do banco de dados
DATABASE_PATH=/app/data/wol_system.db

# Chave secreta (gere uma nova)
SECRET_KEY=sua-chave-secreta-aqui

# Intervalo de monitoramento (segundos)
MONITORING_INTERVAL=60
```

### Personalização da Rede
Edite `docker-compose.yml` para configuração de rede:

```yaml
networks:
  - host  # Para acesso à rede local
# ou
networks:
  custom:
    driver: bridge
```

### Backup do Banco de Dados
```bash
# Backup
docker-compose exec wol-system cp /app/data/wol_system.db /app/data/backup.db

# Restaurar
docker-compose exec wol-system cp /app/data/backup.db /app/data/wol_system.db
```

## 🔒 Segurança

### Recomendações de Segurança
1. **Altere a senha padrão** imediatamente após a instalação
2. **Use HTTPS** em produção (configure reverse proxy)
3. **Restrinja acesso** apenas à rede local ou VPN
4. **Mantenha backups** regulares do banco de dados
5. **Monitore logs** de acesso e atividades

### Configuração de Firewall
Certifique-se de que apenas as portas necessárias estejam abertas:
- Porta da aplicação web (padrão: 5000)
- Porta 9 (UDP) para Wake-on-LAN

## 🐛 Solução de Problemas

### WOL Não Funciona
1. Verifique se WOL está habilitado na BIOS do dispositivo de destino
2. Configure a placa de rede para "Wake on Magic Packet"
3. Certifique-se de que o dispositivo está em suspensão, não desligado completamente
4. Verifique se o cabo de rede está conectado

### Dispositivo Não Aparece como Online
1. Verifique conectividade de rede
2. Confirme se o ping está habilitado no dispositivo de destino
3. Verifique configurações de firewall

### Erro de Permissão
1. Verifique se o usuário está no grupo correto
2. Confirme se o dispositivo está associado ao grupo do usuário
3. Verifique se a conta do usuário está ativa

## 📊 Monitoramento e Logs

### Logs do Sistema
```bash
# Ver logs em tempo real
docker-compose logs -f wol-system

# Ver logs específicos
docker-compose exec wol-system tail -f /var/log/wol_system.log
```

### Métricas
- Dashboard mostra estatísticas em tempo real
- Logs de atividades são mantidos no banco de dados
- Histórico de status dos dispositivos

## 🔄 Atualizações

### Atualizar o Sistema
```bash
# Parar o serviço
docker-compose down

# Baixar atualizações
git pull

# Reconstruir e iniciar
docker-compose up -d --build
```

### Backup Antes de Atualizações
```bash
# Backup completo
docker-compose exec wol-system tar -czf /app/data/backup-$(date +%Y%m%d).tar.gz /app/data/
```

## 📞 Suporte

### Informações de Debug
Para reportar problemas, inclua:
- Versão do Docker
- Logs do container
- Configuração de rede
- Descrição detalhada do problema

### Estrutura de Arquivos
```
web_wol_client/
├── app/
│   ├── models.py          # Modelos do banco de dados
│   ├── forms.py           # Formulários web
│   ├── network.py         # Funções de rede e WOL
│   ├── templates/         # Templates HTML
│   └── static/           # CSS e JavaScript
├── data/                 # Banco de dados SQLite
├── docker-compose.yml    # Configuração Docker
├── Dockerfile           # Imagem Docker
├── requirements.txt     # Dependências Python
└── app.py              # Aplicação principal
```

## 📄 Licença

Este projeto é fornecido "como está" para uso pessoal e educacional.

## 🏆 Recursos Futuros

- [ ] API REST completa
- [ ] Notificações por email/webhook
- [ ] Dashboard com gráficos
- [ ] Agendamento de tarefas
- [ ] Integração com sistemas de monitoramento
- [ ] App mobile
- [ ] Suporte a comandos remotos avançados
