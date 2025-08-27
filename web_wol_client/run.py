#!/usr/bin/env python3
"""
Script de inicialização do Sistema WOL
"""

import os
import sys
from app.main import create_app

# Criar aplicação para o gunicorn
app = create_app()

def main():
    """Função principal para inicializar a aplicação"""
    print("🚀 Iniciando Sistema WOL...")
    
    # Criar diretório de dados se não existir
    data_dir = os.path.join(os.getcwd(), "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"📁 Diretório {data_dir} criado")
    
    # Definir caminho do banco de dados
    db_path = os.path.join(data_dir, "wol_system.db")
    os.environ['DATABASE_PATH'] = db_path
    
    print("✅ Sistema WOL inicializado com sucesso!")
    print(f"💾 Banco de dados: {db_path}")
    print("🌐 Acesse: http://localhost:5000")
    print("👤 Login padrão: admin / admin123")
    print("⚠️  IMPORTANTE: Altere a senha padrão após o primeiro login!")
    
    try:
        # Iniciar servidor de desenvolvimento
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        print("\n🛑 Sistema WOL finalizado pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar sistema: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
