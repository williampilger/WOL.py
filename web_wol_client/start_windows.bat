@echo off
echo ================================================
echo 🚀 Sistema WOL - Inicializacao para Windows
echo ================================================
echo.

REM Verificar se Python está instalado
echo 📋 Verificando instalacao do Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python nao encontrado!
    echo.
    echo Para instalar Python:
    echo 1. Acesse: https://python.org/downloads/
    echo 2. Baixe Python 3.11 ou superior
    echo 3. Durante a instalacao, marque "Add Python to PATH"
    echo 4. Reinicie o prompt de comando e execute este script novamente
    echo.
    pause
    exit /b 1
)

REM Obter versão do Python
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% encontrado

REM Verificar se pip está disponível
echo 📦 Verificando pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip nao encontrado!
    echo Reinstale Python marcando "Add Python to PATH"
    pause
    exit /b 1
)
echo ✅ pip encontrado

REM Criar diretório de dados se não existir
echo 📁 Criando diretorio de dados...
if not exist "data" mkdir data
echo ✅ Diretorio data criado

REM Verificar se virtual environment existe
if not exist "venv" (
    echo � Criando ambiente virtual Python...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Erro ao criar ambiente virtual!
        echo Verifique se Python esta instalado corretamente
        pause
        exit /b 1
    )
    echo ✅ Ambiente virtual criado em .\venv
) else (
    echo ✅ Ambiente virtual ja existe
)

REM Ativar ambiente virtual
echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Erro ao ativar ambiente virtual!
    pause
    exit /b 1
)

REM Verificar se requirements.txt existe
if not exist "requirements.txt" (
    echo ❌ Arquivo requirements.txt nao encontrado!
    pause
    exit /b 1
)

REM Atualizar pip e instalar dependências
echo 📥 Atualizando pip...
python -m pip install --upgrade pip

echo 📦 Instalando dependencias Python...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Erro ao instalar dependencias!
    echo Verifique sua conexao com a internet e tente novamente
    pause
    exit /b 1
)

REM Configurar variáveis de ambiente para Windows
set DATABASE_PATH=%cd%\data\wol_system.db
set FLASK_APP=run.py
set FLASK_ENV=development

echo.
echo ================================================
echo ✅ Sistema WOL configurado com sucesso!
echo ================================================
echo 💾 Banco de dados: %DATABASE_PATH%
echo 🌐 Acesse: http://localhost:5000
echo 👤 Login padrao: admin / admin123
echo ⚠️  IMPORTANTE: Altere a senha padrao apos o primeiro login!
echo ================================================
echo.

REM Perguntar se quer iniciar o servidor
set /p "START_SERVER=Deseja iniciar o servidor agora? (s/N): "
if /i "%START_SERVER%"=="s" (
    echo.
    echo 🚀 Iniciando Sistema WOL...
    echo Para parar o servidor, pressione Ctrl+C
    echo.
    
    REM Executar aplicação
    python run.py
) else (
    echo.
    echo ℹ️  Para iniciar o servidor manualmente:
    echo   venv\Scripts\activate.bat
    echo   python run.py
    echo.
    echo ℹ️  Para usar o ambiente virtual em futuras execucoes:
    echo   venv\Scripts\activate.bat
)

echo.
pause
