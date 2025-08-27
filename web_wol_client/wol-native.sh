#!/bin/bash

# Script de Gerenciamento do Sistema WOL (Execução Nativa)
# Uso: ./wol-native.sh [start|stop|restart|status|logs|backup|update]

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PROJECT_DIR=$(pwd)
VENV_PATH="$PROJECT_DIR/venv"
PID_FILE="$PROJECT_DIR/wol_system.pid"
LOG_FILE="$PROJECT_DIR/wol_system.log"

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Verificar se ambiente virtual existe
check_venv() {
    if [ ! -d "$VENV_PATH" ]; then
        print_error "Ambiente virtual não encontrado!"
        echo "Execute ./start_linux.sh primeiro para configurar o ambiente"
        exit 1
    fi
}

# Ativar ambiente virtual
activate_venv() {
    source "$VENV_PATH/bin/activate"
}

# Verificar se o processo está rodando
is_running() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            return 0
        else
            rm -f "$PID_FILE"
            return 1
        fi
    fi
    return 1
}

case "$1" in
    start)
        print_info "Iniciando Sistema WOL..."
        
        if is_running; then
            print_warning "Sistema já está rodando (PID: $(cat $PID_FILE))"
            exit 0
        fi
        
        check_venv
        activate_venv
        
        # Configurar variáveis de ambiente
        export DATABASE_PATH="$PROJECT_DIR/data/wol_system.db"
        export FLASK_APP=run.py
        export FLASK_ENV=development
        
        # Iniciar em background
        nohup python run.py > "$LOG_FILE" 2>&1 &
        echo $! > "$PID_FILE"
        
        sleep 2
        
        if is_running; then
            print_success "Sistema iniciado com sucesso!"
            print_info "PID: $(cat $PID_FILE)"
            print_info "Acesse: http://localhost:5000"
            print_info "Logs: tail -f $LOG_FILE"
        else
            print_error "Falha ao iniciar o sistema"
            exit 1
        fi
        ;;
        
    stop)
        print_info "Parando Sistema WOL..."
        
        if is_running; then
            PID=$(cat "$PID_FILE")
            kill $PID
            sleep 2
            
            if ! is_running; then
                rm -f "$PID_FILE"
                print_success "Sistema parado com sucesso"
            else
                print_warning "Forçando parada..."
                kill -9 $PID
                rm -f "$PID_FILE"
                print_success "Sistema forçado a parar"
            fi
        else
            print_warning "Sistema não está rodando"
        fi
        ;;
        
    restart)
        print_info "Reiniciando Sistema WOL..."
        $0 stop
        sleep 2
        $0 start
        ;;
        
    status)
        if is_running; then
            PID=$(cat "$PID_FILE")
            print_success "Sistema WOL está rodando (PID: $PID)"
            print_info "URL: http://localhost:5000"
            
            # Verificar se a porta está sendo usada
            if netstat -tlnp 2>/dev/null | grep -q ":5000 "; then
                print_success "Porta 5000 está ativa"
            else
                print_warning "Porta 5000 não está ativa"
            fi
        else
            print_error "Sistema WOL não está rodando"
        fi
        ;;
        
    logs)
        if [ -f "$LOG_FILE" ]; then
            print_info "Logs do Sistema WOL (Ctrl+C para sair):"
            tail -f "$LOG_FILE"
        else
            print_error "Arquivo de log não encontrado"
        fi
        ;;
        
    backup)
        DB_FILE="$PROJECT_DIR/data/wol_system.db"
        if [ -f "$DB_FILE" ]; then
            BACKUP_NAME="backup-$(date +%Y%m%d-%H%M%S).db"
            BACKUP_PATH="$PROJECT_DIR/data/$BACKUP_NAME"
            
            cp "$DB_FILE" "$BACKUP_PATH"
            print_success "Backup criado: $BACKUP_PATH"
        else
            print_error "Banco de dados não encontrado"
        fi
        ;;
        
    update)
        print_info "Atualizando Sistema WOL..."
        
        if is_running; then
            print_info "Parando sistema..."
            $0 stop
            RESTART_AFTER=true
        fi
        
        check_venv
        activate_venv
        
        print_info "Atualizando dependências..."
        pip install -r requirements.txt --upgrade
        
        if [ "$RESTART_AFTER" = true ]; then
            print_info "Reiniciando sistema..."
            $0 start
        fi
        
        print_success "Sistema atualizado com sucesso"
        ;;
        
    *)
        echo "Sistema WOL - Gerenciador Nativo"
        echo "Uso: $0 {start|stop|restart|status|logs|backup|update}"
        echo ""
        echo "Comandos disponíveis:"
        echo "  start   - Iniciar o sistema em background"
        echo "  stop    - Parar o sistema"
        echo "  restart - Reiniciar o sistema"
        echo "  status  - Verificar status do sistema"
        echo "  logs    - Visualizar logs em tempo real"
        echo "  backup  - Criar backup do banco de dados"
        echo "  update  - Atualizar dependências"
        echo ""
        echo "Arquivos importantes:"
        echo "  PID: $PID_FILE"
        echo "  Logs: $LOG_FILE"
        echo "  Banco: $PROJECT_DIR/data/wol_system.db"
        exit 1
        ;;
esac
