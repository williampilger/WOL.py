@echo off
echo 🚀 Iniciando Sistema WOL no Windows...
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado! Instale Python 3.11 ou superior.
    echo    Download: https://python.org
    pause
    exit /b 1
)

REM Criar diretório de dados se não existir
if not exist "data" mkdir data

REM Instalar dependências se não existir virtual environment
if not exist "venv" (
    echo 📦 Criando ambiente virtual...
    python -m venv venv
    echo ✅ Ambiente virtual criado!
)

REM Ativar ambiente virtual
echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Instalar dependências
echo 📥 Instalando dependências...
pip install -r requirements.txt

REM Configurar variáveis de ambiente para Windows
set DATABASE_PATH=data\wol_system.db
set FLASK_APP=run.py
set FLASK_ENV=development

echo.
echo ✅ Sistema WOL configurado com sucesso!
echo 💾 Banco de dados: %cd%\data\wol_system.db
echo 🌐 Acesse: http://localhost:5000
echo 👤 Login padrão: admin / admin123
echo ⚠️  IMPORTANTE: Altere a senha padrão após o primeiro login!
echo.
echo 🚀 Iniciando servidor...

REM Executar aplicação
python run.py

pause
