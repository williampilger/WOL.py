#!/bin/bash

# Script de gerenciamento do Sistema WOL
# Uso: ./wol-manager.sh [start|stop|restart|logs|backup|update]

COMPOSE_FILE="docker-compose.yml"
SERVICE_NAME="wol-system"

case "$1" in
    start)
        echo "🚀 Iniciando Sistema WOL..."
        docker-compose up -d
        echo "✅ Sistema iniciado! Acesse: http://localhost:5000"
        echo "👤 Login padrão: admin / admin123"
        ;;
    
    stop)
        echo "🛑 Parando Sistema WOL..."
        docker-compose down
        echo "✅ Sistema parado"
        ;;
    
    restart)
        echo "🔄 Reiniciando Sistema WOL..."
        docker-compose restart
        echo "✅ Sistema reiniciado"
        ;;
    
    logs)
        echo "📋 Logs do Sistema WOL:"
        docker-compose logs -f
        ;;
    
    backup)
        echo "💾 Criando backup do banco de dados..."
        BACKUP_NAME="backup-$(date +%Y%m%d-%H%M%S).db"
        docker-compose exec $SERVICE_NAME cp /app/data/wol_system.db /app/data/$BACKUP_NAME
        echo "✅ Backup criado: data/$BACKUP_NAME"
        ;;
    
    update)
        echo "🔄 Atualizando Sistema WOL..."
        docker-compose down
        docker-compose pull
        docker-compose up -d --build
        echo "✅ Sistema atualizado"
        ;;
    
    status)
        echo "📊 Status do Sistema WOL:"
        docker-compose ps
        ;;
    
    shell)
        echo "🖥️ Acessando shell do container..."
        docker-compose exec $SERVICE_NAME /bin/bash
        ;;
    
    *)
        echo "Sistema WOL - Gerenciador"
        echo "Uso: $0 {start|stop|restart|logs|backup|update|status|shell}"
        echo ""
        echo "Comandos disponíveis:"
        echo "  start   - Iniciar o sistema"
        echo "  stop    - Parar o sistema"
        echo "  restart - Reiniciar o sistema"
        echo "  logs    - Visualizar logs em tempo real"
        echo "  backup  - Criar backup do banco de dados"
        echo "  update  - Atualizar sistema"
        echo "  status  - Verificar status dos containers"
        echo "  shell   - Acessar shell do container"
        exit 1
        ;;
esac
