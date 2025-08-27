# Sistema WOL - Execução Nativa (sem Docker)

Este guia mostra como executar o Sistema WOL diretamente com Python, sem usar Docker, tanto no Windows quanto no Linux.

## 📋 Pré-requisitos

### Para Windows e Linux
- **Python 3.11 ou superior**
- **pip** (gerenciador de pacotes Python)
- **Conexão com a internet** (para instalação de dependências)

### Apenas para Linux
- **nmap** (será instalado automaticamente pelo script)
- **Permissões sudo** (para instalar nmap se necessário)

## 🚀 Instalação Rápida

### Windows
1. **Execute o script automático**:
   ```cmd
   start_windows.bat
   ```
   
   O script irá:
   - ✅ Verificar se Python está instalado
   - ✅ Criar ambiente virtual automaticamente
   - ✅ Instalar todas as dependências
   - ✅ Configurar variáveis de ambiente
   - ✅ Oferecer para iniciar o servidor

### Linux
1. **Execute o script automático**:
   ```bash
   ./start_linux.sh
   ```
   
   O script irá:
   - ✅ Verificar se Python 3.11+ está instalado
   - ✅ Instalar nmap se necessário
   - ✅ Criar ambiente virtual automaticamente
   - ✅ Instalar todas as dependências
   - ✅ Configurar variáveis de ambiente
   - ✅ Oferecer para iniciar o servidor

## 🛠️ Instalação Manual

Se preferir fazer a instalação passo a passo:

### 1. Verificar Python

**Windows:**
```cmd
python --version
```

**Linux:**
```bash
python3 --version
```

### 2. Instalar Dependências do Sistema

**Apenas Linux:**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip python3-venv nmap

# CentOS/RHEL/Fedora
sudo dnf install python3 python3-pip nmap
```

### 3. Criar Ambiente Virtual

**Windows:**
```cmd
python -m venv venv
```

**Linux:**
```bash
python3 -m venv venv
```

### 4. Ativar Ambiente Virtual

**Windows:**
```cmd
venv\Scripts\activate.bat
```

**Linux:**
```bash
source venv/bin/activate
```

### 5. Instalar Dependências Python

**Windows e Linux:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Criar Diretório de Dados

**Windows:**
```cmd
mkdir data
```

**Linux:**
```bash
mkdir -p data
```

### 7. Executar Sistema

**Windows e Linux:**
```bash
python run.py
```

## 🌐 Acessando o Sistema

Após executar qualquer um dos métodos acima:

- **URL**: http://localhost:5000
- **Login**: admin
- **Senha**: admin123

⚠️ **IMPORTANTE**: Altere a senha padrão após o primeiro login!

## 🔧 Uso do Ambiente Virtual

### Por que usar ambiente virtual?

O ambiente virtual (venv) isola as dependências do projeto, evitando conflitos com outras instalações Python no sistema.

### Como ativar/desativar

**Ativar (Windows):**
```cmd
venv\Scripts\activate.bat
```

**Ativar (Linux):**
```bash
source venv/bin/activate
```

**Desativar (ambos):**
```bash
deactivate
```

### Indicador Visual

Quando o ambiente virtual está ativo, você verá `(venv)` no início do prompt:

**Windows:**
```cmd
(venv) C:\caminho\para\projeto>
```

**Linux:**
```bash
(venv) user@computer:~/projeto$
```

## 📁 Estrutura de Arquivos

```
projeto/
├── start_windows.bat     ← Script automático para Windows
├── start_linux.sh       ← Script automático para Linux
├── run.py               ← Script principal de inicialização
├── requirements.txt     ← Dependências Python
├── venv/               ← Ambiente virtual (criado automaticamente)
│   ├── Scripts/        ← Executáveis (Windows)
│   ├── bin/           ← Executáveis (Linux)
│   └── lib/           ← Bibliotecas Python
├── app/               ← Código da aplicação
│   ├── main.py        ← Aplicação Flask principal
│   ├── models.py      ← Modelos do banco de dados
│   ├── forms.py       ← Formulários web
│   ├── network.py     ← Funcionalidades de rede
│   ├── templates/     ← Templates HTML
│   └── static/        ← Arquivos CSS/JS
└── data/              ← Banco de dados (criado automaticamente)
    └── wol_system.db  ← Arquivo SQLite
```

## 🐛 Solução de Problemas

### Windows

#### "python não é reconhecido"
1. Reinstale Python de https://python.org
2. ✅ Marque "Add Python to PATH" durante a instalação
3. Reinicie o Prompt de Comando

#### "pip não é reconhecido"
```cmd
python -m pip install --upgrade pip
```

#### Erro de permissão
Execute o Prompt de Comando como Administrador

### Linux

#### "python3: command not found"
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip python3-venv

# CentOS/RHEL/Fedora
sudo dnf install python3 python3-pip
```

#### "Permission denied" no script
```bash
chmod +x start_linux.sh
./start_linux.sh
```

#### Erro com nmap
```bash
# Ubuntu/Debian
sudo apt install nmap

# CentOS/RHEL/Fedora
sudo dnf install nmap
```

### Problemas Gerais

#### Erro ao instalar dependências
1. Verifique conexão com a internet
2. Atualize pip: `pip install --upgrade pip`
3. Tente instalar individualmente: `pip install flask`

#### Banco de dados corrompido
1. Pare o servidor (Ctrl+C)
2. Delete o arquivo `data/wol_system.db`
3. Reinicie o servidor - será criado novo banco

#### Porta 5000 já em uso
1. Encontre o processo: 
   - Windows: `netstat -ano | findstr :5000`
   - Linux: `sudo netstat -tulpn | grep :5000`
2. Finalize o processo ou use porta diferente

## 🔒 Segurança

### Recomendações
- ✅ Altere a senha padrão imediatamente
- ✅ Use apenas em redes confiáveis
- ✅ Configure firewall adequadamente
- ⚠️ Não exponha para internet sem configurações adicionais

### Firewall Windows
Se o Windows bloquear acesso:
1. Vá em **Configurações** → **Rede e Internet** → **Firewall**
2. Clique em **Permitir aplicativo pelo firewall**
3. Adicione Python.exe se solicitado

## 💡 Dicas de Uso

### Primeira Execução
1. **Cadastre dispositivos** com IPs fixos
2. **Habilite Wake-on-LAN** na BIOS dos PCs alvo
3. **Configure grupos** para organizar dispositivos
4. **Teste WOL** com dispositivos próximos primeiro

### Monitoramento Automático
- O sistema monitora dispositivos automaticamente a cada 60 segundos
- Apenas dispositivos com "Monitoramento por Ping" habilitado são verificados
- Status é atualizado em tempo real no Dashboard

### Funcionalidades Principais
- **Wake-on-LAN**: Ligar PCs remotamente
- **Ping Monitoring**: Verificação automática de status
- **Network Scan**: Descoberta de dispositivos na rede
- **User Management**: Controle de acesso por usuários e grupos
- **Activity Logs**: Histórico completo de ações

### Performance
- Use cabos de rede para melhor confiabilidade do WOL
- Configure IPs fixos nos dispositivos de destino
- Evite usar WiFi para dispositivos críticos
- Mantenha o servidor na mesma rede dos dispositivos

## 🔄 Gerenciamento do Sistema

### Scripts de Gerenciamento

Depois da instalação inicial, você pode usar scripts de conveniência para gerenciar o sistema:

#### Windows (PowerShell)
```powershell
# Iniciar sistema em background
.\wol-native.ps1 start

# Parar sistema
.\wol-native.ps1 stop

# Reiniciar sistema
.\wol-native.ps1 restart

# Verificar status
.\wol-native.ps1 status

# Ver logs em tempo real
.\wol-native.ps1 logs

# Criar backup do banco
.\wol-native.ps1 backup

# Atualizar dependências
.\wol-native.ps1 update
```

#### Linux
```bash
# Iniciar sistema em background
./wol-native.sh start

# Parar sistema
./wol-native.sh stop

# Reiniciar sistema
./wol-native.sh restart

# Verificar status
./wol-native.sh status

# Ver logs em tempo real
./wol-native.sh logs

# Criar backup do banco
./wol-native.sh backup

# Atualizar dependências
./wol-native.sh update
```

### Execução Manual

Se preferir controle total:

**Ativar ambiente virtual:**
- Windows: `venv\Scripts\activate.bat`
- Linux: `source venv/bin/activate`

**Executar sistema:**
```bash
python run.py
```

**Executar em background (Linux):**
```bash
nohup python run.py > wol_system.log 2>&1 &
```

## 🔄 Atualizações

Para atualizar o sistema:

1. **Ativar ambiente virtual**
2. **Atualizar dependências**: `pip install -r requirements.txt --upgrade`
3. **Reiniciar aplicação**

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs no terminal
2. Confirme que todas as dependências estão instaladas
3. Teste com dispositivos simples primeiro
4. Verifique configurações de rede e firewall
