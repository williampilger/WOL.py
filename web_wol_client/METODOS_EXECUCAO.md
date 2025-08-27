# 🚀 Sistema WOL - Métodos de Execução

## 📋 Resumo das Opções

| Método | Windows | Linux | Complexidade | Recomendado Para |
|--------|---------|--------|--------------|------------------|
| **Docker** | ✅ | ✅ | Baixa | Produção |
| **Script Automático** | ✅ | ✅ | Baixa | Desenvolvimento |
| **Manual** | ✅ | ✅ | Média | Aprendizado |

## 🐳 Método 1: Docker (Recomendado para Produção)

### Vantagens
- ✅ Isolamento completo
- ✅ Fácil deploy e atualização
- ✅ Funciona igual em qualquer OS
- ✅ Inclui todas as dependências
- ✅ Backup e restore simples

### Como usar
```bash
# Iniciar
./wol-manager.sh start

# Parar
./wol-manager.sh stop

# Ver logs
./wol-manager.sh logs

# Backup
./wol-manager.sh backup
```

### Quando usar
- ✅ Servidores de produção
- ✅ Ambiente empresarial
- ✅ Múltiplas instalações
- ✅ Quando quer "instalar e esquecer"

---

## 🖥️ Método 2: Execução Nativa com Scripts

### Vantagens
- ✅ Controle total do ambiente
- ✅ Mais fácil para debug
- ✅ Acesso direto aos logs
- ✅ Customização avançada
- ✅ Menor uso de recursos

### Windows
```cmd
# Instalação inicial
start_windows.bat

# Gerenciamento
.\wol-native.ps1 start
.\wol-native.ps1 status
.\wol-native.ps1 logs
```

### Linux
```bash
# Instalação inicial
./start_linux.sh

# Gerenciamento
./wol-native.sh start
./wol-native.sh status
./wol-native.sh logs
```

### Quando usar
- ✅ Desenvolvimento e testes
- ✅ Ambiente doméstico
- ✅ Quando precisa de customização
- ✅ Debug e troubleshooting

---

## ⚙️ Método 3: Execução Manual

### Vantagens
- ✅ Máximo controle
- ✅ Entendimento completo
- ✅ Flexibilidade total
- ✅ Bom para aprender

### Passo a passo
```bash
# 1. Criar ambiente virtual
python -m venv venv

# 2. Ativar ambiente
# Windows: venv\Scripts\activate.bat
# Linux: source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar
python run.py
```

### Quando usar
- ✅ Primeira experiência com Python
- ✅ Ambiente de desenvolvimento específico
- ✅ Integração com outros sistemas
- ✅ Troubleshooting avançado

---

## 🎯 Guia de Decisão

### Para Produção → Use Docker
```bash
git clone <repo>
cd web_wol_client
./wol-manager.sh start
```

### Para Desenvolvimento → Use Scripts
**Windows:**
```cmd
git clone <repo>
cd web_wol_client
start_windows.bat
```

**Linux:**
```bash
git clone <repo>
cd web_wol_client
./start_linux.sh
```

### Para Aprendizado → Execução Manual
Siga o guia detalhado em [`INSTALACAO_NATIVA.md`](INSTALACAO_NATIVA.md)

---

## 📁 Estrutura de Arquivos por Método

### Docker
```
projeto/
├── docker-compose.yml    ← Configuração principal
├── Dockerfile           ← Imagem do container
├── wol-manager.sh       ← Script de gerenciamento
└── ...
```

### Scripts Automáticos
```
projeto/
├── start_windows.bat    ← Instalação Windows
├── start_linux.sh       ← Instalação Linux
├── wol-native.ps1       ← Gerenciamento Windows
├── wol-native.sh        ← Gerenciamento Linux
├── venv/               ← Ambiente virtual (criado)
└── ...
```

### Manual
```
projeto/
├── requirements.txt     ← Dependências
├── run.py              ← Script principal
├── venv/               ← Ambiente virtual (você cria)
└── app/                ← Código da aplicação
```

---

## 🆘 Troubleshooting Rápido

| Problema | Docker | Nativo |
|----------|--------|--------|
| **Porta ocupada** | `docker-compose down` | `./wol-native.sh stop` |
| **Dependências** | `docker-compose build` | `pip install -r requirements.txt` |
| **Logs** | `docker-compose logs` | `./wol-native.sh logs` |
| **Backup** | `./wol-manager.sh backup` | `./wol-native.sh backup` |
| **Atualizar** | `./wol-manager.sh update` | `./wol-native.sh update` |

---

## 🔒 Segurança por Método

### Docker
- ✅ Isolamento de rede
- ✅ Container sem privilégios
- ✅ Volumes mapeados específicos

### Nativo
- ⚠️ Acesso direto ao sistema
- ⚠️ Dependências globais
- ✅ Controle total de permissões

### Recomendação
- **Produção**: Docker com reverse proxy (nginx)
- **Desenvolvimento**: Nativo com firewall configurado
- **Teste**: Qualquer método em rede isolada

---

## ⚡ Performance por Método

### Docker
- **RAM**: ~200MB (container + app)
- **CPU**: Baixo overhead
- **Disco**: ~500MB (imagem + dados)
- **Rede**: Overhead mínimo

### Nativo
- **RAM**: ~50MB (apenas app)
- **CPU**: Overhead zero
- **Disco**: ~100MB (venv + dados)
- **Rede**: Acesso direto

### Conclusão
- Para **máxima performance**: Nativo
- Para **melhor isolamento**: Docker
- Para **facilidade**: Scripts automáticos
