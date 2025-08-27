# 📋 Arquivos de Instalação e Execução

## 🐳 Docker
- `docker-compose.yml` - Configuração do container
- `Dockerfile` - Imagem do sistema  
- `wol-manager.sh` - Script de gerenciamento Docker

## 🪟 Windows
- `start_windows.bat` - Instalação automática
- `wol-native.ps1` - Gerenciamento (PowerShell)
- `WINDOWS_SETUP.md` - Guia específico Windows

## 🐧 Linux  
- `start_linux.sh` - Instalação automática
- `wol-native.sh` - Gerenciamento (Bash)

## 📚 Documentação
- `README.md` - Documentação principal
- `INSTALACAO_NATIVA.md` - Guia detalhado execução nativa
- `METODOS_EXECUCAO.md` - Comparação dos métodos
- `ARQUIVOS_SISTEMA.md` - Este arquivo

## ⚙️ Sistema Principal
- `run.py` - Script de inicialização
- `requirements.txt` - Dependências Python
- `app/` - Código da aplicação Flask

## 🗃️ Dados
- `data/` - Banco de dados SQLite (criado automaticamente)
- `.env.example` - Exemplo de configuração

## ⚡ Execução Rápida

### Primeira vez (escolha um):
```bash
# Docker
./wol-manager.sh start

# Windows
start_windows.bat

# Linux  
./start_linux.sh
```

### Uso diário:
```bash
# Docker
./wol-manager.sh [start|stop|logs|backup]

# Windows
.\wol-native.ps1 [start|stop|logs|backup]

# Linux
./wol-native.sh [start|stop|logs|backup]
```

## 🔍 Localização dos Arquivos

### Logs
- **Docker**: `docker-compose logs`
- **Nativo**: `wol_system.log` 

### Banco de Dados
- **Docker**: Volume `./data/wol_system.db`
- **Nativo**: `./data/wol_system.db`

### Configuração
- **Docker**: `docker-compose.yml`
- **Nativo**: Variáveis de ambiente nos scripts
