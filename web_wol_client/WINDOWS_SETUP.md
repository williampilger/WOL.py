# Como Executar o Sistema WOL no Windows

## 📋 Pré-requisitos

1. **Python 3.11 ou superior** instalado no Windows
   - Download: https://python.org
   - ✅ Certifique-se de marcar "Add Python to PATH" durante a instalação

2. **Git** (opcional, para clonar o repositório)
   - Download: https://git-scm.com/download/win

## 🚀 Instalação Rápida (Método Simples)

### Opção 1: Script Automático (Recomendado)
1. Baixe ou clone este projeto para uma pasta no Windows
2. **Duplo-clique no arquivo `start_windows.bat`**
3. O script irá:
   - ✅ Verificar se Python está instalado
   - ✅ Criar ambiente virtual automaticamente
   - ✅ Instalar todas as dependências
   - ✅ Configurar o banco de dados
   - ✅ Iniciar o servidor web

### Opção 2: Manual via Prompt de Comando
```cmd
# 1. Abrir Prompt de Comando (cmd) na pasta do projeto
cd C:\caminho\para\seu\projeto

# 2. Criar ambiente virtual
python -m venv venv

# 3. Ativar ambiente virtual
venv\Scripts\activate.bat

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Executar o sistema
python run.py
```

## 🌐 Acessando o Sistema

Após executar qualquer uma das opções acima:
- **URL**: http://localhost:5000
- **Login**: admin
- **Senha**: admin123

## 🛠️ Configurações Específicas do Windows

### Firewall do Windows
O Windows pode bloquear o acesso à rede. Se necessário:
1. Vá em **Configurações** → **Rede e Internet** → **Firewall do Windows Defender**
2. Clique em **Permitir um aplicativo pelo firewall**
3. Adicione Python.exe se solicitado

### Permissões de Administrador
Para algumas funcionalidades de rede avançadas, execute o Prompt de Comando como **Administrador**.

### Dependências de Rede
O sistema usa as seguintes bibliotecas para funcionalidades de rede:
- `python-nmap`: Para scan de rede
- `ping3`: Para verificação de status
- `wakeonlan`: Para Wake-on-LAN

### Solução de Problemas

#### Erro: "python não é reconhecido"
- Reinstale Python marcando "Add Python to PATH"
- Ou adicione Python ao PATH manualmente

#### Erro: "pip não é reconhecido"  
- Python foi instalado corretamente mas pip não está no PATH
- Use: `python -m pip install -r requirements.txt`

#### Problemas de Rede
- Verifique se o PC está na mesma rede dos dispositivos alvo
- Desative temporariamente o firewall para teste
- Alguns antivírus podem bloquear scan de rede

## 📁 Estrutura de Arquivos Importante

```
web_wol_client/
├── start_windows.bat     ← Execute este arquivo no Windows
├── run.py               ← Script principal de inicialização  
├── requirements.txt     ← Dependências Python
├── app/                 ← Código da aplicação
│   ├── main.py         ← Aplicação Flask principal
│   ├── models.py       ← Modelos do banco de dados
│   ├── forms.py        ← Formulários web
│   ├── network.py      ← Funcionalidades de rede
│   └── templates/      ← Templates HTML
└── data/               ← Banco de dados (criado automaticamente)
    └── wol_system.db   ← Arquivo SQLite
```

## 🐳 Alternativa: Docker no Windows

Se preferir usar Docker:
1. Instale **Docker Desktop for Windows**
2. Execute no PowerShell:
   ```powershell
   docker-compose up --build
   ```

## 🔒 Segurança

⚠️ **IMPORTANTE**: 
- Altere a senha padrão (`admin123`) imediatamente após o primeiro login
- O sistema por padrão roda apenas na rede local (localhost)
- Para acesso remoto, configure adequadamente firewall e segurança

## 💡 Dicas de Uso

1. **Configure IPs fixos** nos dispositivos que quer controlar
2. **Habilite Wake-on-LAN** na BIOS de cada dispositivo
3. **Use cabos de rede** para melhor confiabilidade do WOL
4. **Teste primeiro** com dispositivos próximos antes de usar em produção
