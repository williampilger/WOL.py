# Script de Gerenciamento do Sistema WOL (Execução Nativa) - Windows PowerShell
# Uso: .\wol-native.ps1 [start|stop|restart|status|logs|backup|update]

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("start", "stop", "restart", "status", "logs", "backup", "update")]
    [string]$Action
)

$ProjectDir = $PSScriptRoot
$VenvPath = Join-Path $ProjectDir "venv"
$PidFile = Join-Path $ProjectDir "wol_system.pid"
$LogFile = Join-Path $ProjectDir "wol_system.log"

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ️  $Message" -ForegroundColor Blue
}

function Write-Warning-Custom {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor Yellow
}

function Test-VenvExists {
    if (-not (Test-Path $VenvPath)) {
        Write-Error-Custom "Ambiente virtual não encontrado!"
        Write-Host "Execute start_windows.bat primeiro para configurar o ambiente"
        exit 1
    }
}

function Test-IsRunning {
    if (Test-Path $PidFile) {
        $pid = Get-Content $PidFile -ErrorAction SilentlyContinue
        if ($pid -and (Get-Process -Id $pid -ErrorAction SilentlyContinue)) {
            return $true
        } else {
            Remove-Item $PidFile -ErrorAction SilentlyContinue
            return $false
        }
    }
    return $false
}

function Start-WolSystem {
    Write-Info "Iniciando Sistema WOL..."
    
    if (Test-IsRunning) {
        $pid = Get-Content $PidFile
        Write-Warning-Custom "Sistema já está rodando (PID: $pid)"
        return
    }
    
    Test-VenvExists
    
    # Ativar ambiente virtual e executar
    $activateScript = Join-Path $VenvPath "Scripts\Activate.ps1"
    if (-not (Test-Path $activateScript)) {
        Write-Error-Custom "Script de ativação do ambiente virtual não encontrado"
        return
    }
    
    # Configurar variáveis de ambiente
    $env:DATABASE_PATH = Join-Path $ProjectDir "data\wol_system.db"
    $env:FLASK_APP = "run.py"
    $env:FLASK_ENV = "development"
    
    # Iniciar processo em background
    $startInfo = New-Object System.Diagnostics.ProcessStartInfo
    $startInfo.FileName = Join-Path $VenvPath "Scripts\python.exe"
    $startInfo.Arguments = "run.py"
    $startInfo.WorkingDirectory = $ProjectDir
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    $startInfo.UseShellExecute = $false
    $startInfo.CreateNoWindow = $true
    
    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $startInfo
    $process.Start()
    
    # Salvar PID
    $process.Id | Out-File -FilePath $PidFile -Encoding ASCII
    
    Start-Sleep 2
    
    if (Test-IsRunning) {
        Write-Success "Sistema iniciado com sucesso!"
        Write-Info "PID: $($process.Id)"
        Write-Info "Acesse: http://localhost:5000"
        Write-Info "Logs: Get-Content $LogFile -Wait"
    } else {
        Write-Error-Custom "Falha ao iniciar o sistema"
    }
}

function Stop-WolSystem {
    Write-Info "Parando Sistema WOL..."
    
    if (Test-IsRunning) {
        $pid = Get-Content $PidFile
        try {
            Stop-Process -Id $pid -Force -ErrorAction Stop
            Start-Sleep 2
            
            if (-not (Test-IsRunning)) {
                Remove-Item $PidFile -ErrorAction SilentlyContinue
                Write-Success "Sistema parado com sucesso"
            }
        } catch {
            Write-Error-Custom "Erro ao parar o processo: $_"
        }
    } else {
        Write-Warning-Custom "Sistema não está rodando"
    }
}

function Show-Status {
    if (Test-IsRunning) {
        $pid = Get-Content $PidFile
        Write-Success "Sistema WOL está rodando (PID: $pid)"
        Write-Info "URL: http://localhost:5000"
        
        # Verificar se a porta está sendo usada
        $port = netstat -an | Select-String ":5000"
        if ($port) {
            Write-Success "Porta 5000 está ativa"
        } else {
            Write-Warning-Custom "Porta 5000 não está ativa"
        }
    } else {
        Write-Error-Custom "Sistema WOL não está rodando"
    }
}

function Show-Logs {
    if (Test-Path $LogFile) {
        Write-Info "Logs do Sistema WOL (Ctrl+C para sair):"
        Get-Content $LogFile -Wait
    } else {
        Write-Error-Custom "Arquivo de log não encontrado"
    }
}

function Create-Backup {
    $dbFile = Join-Path $ProjectDir "data\wol_system.db"
    if (Test-Path $dbFile) {
        $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
        $backupName = "backup-$timestamp.db"
        $backupPath = Join-Path $ProjectDir "data\$backupName"
        
        Copy-Item $dbFile $backupPath
        Write-Success "Backup criado: $backupPath"
    } else {
        Write-Error-Custom "Banco de dados não encontrado"
    }
}

function Update-System {
    Write-Info "Atualizando Sistema WOL..."
    
    $restartAfter = $false
    if (Test-IsRunning) {
        Write-Info "Parando sistema..."
        Stop-WolSystem
        $restartAfter = $true
    }
    
    Test-VenvExists
    
    # Ativar ambiente virtual e atualizar
    $pythonExe = Join-Path $VenvPath "Scripts\python.exe"
    $pipExe = Join-Path $VenvPath "Scripts\pip.exe"
    
    Write-Info "Atualizando dependências..."
    & $pipExe install -r requirements.txt --upgrade
    
    if ($restartAfter) {
        Write-Info "Reiniciando sistema..."
        Start-WolSystem
    }
    
    Write-Success "Sistema atualizado com sucesso"
}

# Executar ação solicitada
switch ($Action) {
    "start" { Start-WolSystem }
    "stop" { Stop-WolSystem }
    "restart" { 
        Stop-WolSystem
        Start-Sleep 2
        Start-WolSystem
    }
    "status" { Show-Status }
    "logs" { Show-Logs }
    "backup" { Create-Backup }
    "update" { Update-System }
}
