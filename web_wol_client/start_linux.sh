#!/bin/bash

# Script de Inicialização do Sistema WOL para Linux
# =================================================

set -e  # Parar execução em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir mensagens coloridas
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Banner
echo "================================================="
echo "🚀 Sistema WOL - Inicialização para Linux"
echo "================================================="
echo ""

# Verificar se Python 3.11+ está instalado
print_info "Verificando instalação do Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 11 ]; then
        print_success "Python $PYTHON_VERSION encontrado"
        PYTHON_CMD="python3"
    else
        print_error "Python 3.11 ou superior é necessário. Versão encontrada: $PYTHON_VERSION"
        echo "Instale Python 3.11+ e tente novamente."
        exit 1
    fi
else
    print_error "Python não encontrado!"
    echo "Para instalar no Ubuntu/Debian:"
    echo "  sudo apt update && sudo apt install python3 python3-pip python3-venv"
    echo "Para instalar no CentOS/RHEL:"
    echo "  sudo yum install python3 python3-pip"
    exit 1
fi

# Verificar se pip está instalado
print_info "Verificando pip..."
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 não encontrado!"
    echo "Instale pip3 com: sudo apt install python3-pip"
    exit 1
fi
print_success "pip3 encontrado"

# Verificar dependências do sistema para nmap
print_info "Verificando dependências do sistema..."
if ! command -v nmap &> /dev/null; then
    print_warning "nmap não encontrado. Instalando..."
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y nmap
    elif command -v yum &> /dev/null; then
        sudo yum install -y nmap
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y nmap
    else
        print_error "Não foi possível instalar nmap automaticamente"
        echo "Instale nmap manualmente e execute este script novamente"
        exit 1
    fi
fi
print_success "nmap encontrado"

# Criar diretório de dados
print_info "Criando diretório de dados..."
mkdir -p data
print_success "Diretório data criado"

# Verificar se virtual environment existe
if [ ! -d "venv" ]; then
    print_info "Criando ambiente virtual Python..."
    $PYTHON_CMD -m venv venv
    print_success "Ambiente virtual criado em ./venv"
else
    print_success "Ambiente virtual já existe"
fi

# Ativar ambiente virtual
print_info "Ativando ambiente virtual..."
source venv/bin/activate

# Verificar se requirements.txt existe
if [ ! -f "requirements.txt" ]; then
    print_error "Arquivo requirements.txt não encontrado!"
    exit 1
fi

# Instalar dependências
print_info "Instalando dependências Python..."
pip install --upgrade pip
pip install -r requirements.txt
print_success "Dependências instaladas"

# Configurar variáveis de ambiente
export DATABASE_PATH="$(pwd)/data/wol_system.db"
export FLASK_APP=run.py
export FLASK_ENV=development

print_success "Ambiente configurado com sucesso!"
echo ""
echo "================================================="
echo "🌐 Informações de Acesso:"
echo "------------------------------------------------"
echo "URL: http://localhost:5000"
echo "Login: admin"
echo "Senha: admin123"
echo "------------------------------------------------"
echo "⚠️  IMPORTANTE: Altere a senha padrão após o primeiro login!"
echo "================================================="
echo ""

# Verificar se o usuário quer iniciar o servidor
read -p "Deseja iniciar o servidor agora? (s/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    print_info "Iniciando Sistema WOL..."
    echo ""
    echo "Para parar o servidor, pressione Ctrl+C"
    echo ""
    
    # Executar servidor
    python run.py
else
    echo ""
    print_info "Para iniciar o servidor manualmente:"
    echo "  source venv/bin/activate"
    echo "  python run.py"
    echo ""
    print_info "Para usar o ambiente virtual em futuras execuções:"
    echo "  source venv/bin/activate"
fi
