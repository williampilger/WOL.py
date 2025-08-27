// JavaScript customizado para o Sistema WOL

// Função para mostrar alertas dinâmicos
function showAlert(type, message, duration = 5000) {
    const alertHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            <i class="fas fa-${getAlertIcon(type)}"></i> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertAdjacentHTML('afterbegin', alertHTML);
        
        // Auto-remove após duration
        if (duration > 0) {
            setTimeout(() => {
                const alert = container.querySelector('.alert');
                if (alert) {
                    const bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                }
            }, duration);
        }
    }
}

// Função para obter ícone do alerta
function getAlertIcon(type) {
    const icons = {
        'success': 'check-circle',
        'danger': 'exclamation-triangle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle',
        'primary': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// Função para confirmar ações de exclusão
function confirmDelete(message = 'Tem certeza que deseja excluir este item?') {
    return confirm(message);
}

// Função para ping de dispositivos com feedback visual
function pingDevice(deviceId, buttonElement = null) {
    if (buttonElement) {
        const originalContent = buttonElement.innerHTML;
        buttonElement.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        buttonElement.disabled = true;
    }
    
    fetch(`/api/ping/${deviceId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert('success', `Ping realizado com sucesso: ${data.message}`);
            } else {
                showAlert('danger', `Erro no ping: ${data.message}`);
            }
            
            // Atualizar status na interface se possível
            updateDeviceStatus(deviceId, data.status);
            
            // Recarregar página após um tempo
            setTimeout(() => location.reload(), 2000);
        })
        .catch(error => {
            console.error('Erro ao realizar ping:', error);
            showAlert('danger', 'Erro ao realizar ping do dispositivo');
        })
        .finally(() => {
            if (buttonElement) {
                buttonElement.innerHTML = originalContent;
                buttonElement.disabled = false;
            }
        });
}

// Função para atualizar status do dispositivo na interface
function updateDeviceStatus(deviceId, status) {
    const statusElement = document.querySelector(`[data-device-id="${deviceId}"] .device-status`);
    if (statusElement) {
        // Atualizar badge de status
        statusElement.className = `badge bg-${status === 'online' ? 'success' : 'danger'} fs-6`;
        statusElement.innerHTML = status === 'online' ? 
            '<i class="fas fa-check-circle"></i> Online' : 
            '<i class="fas fa-times-circle"></i> Offline';
    }
}

// Função para auto-refresh do dashboard
function initAutoRefresh(interval = 60000) {
    if (document.querySelector('[data-auto-refresh="true"]')) {
        setInterval(() => {
            location.reload();
        }, interval);
    }
}

// Função para validar endereços MAC
function validateMacAddress(input) {
    const macPattern = /^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$/;
    const value = input.value.toUpperCase();
    
    if (value && !macPattern.test(value)) {
        input.setCustomValidity('Formato de MAC address inválido. Use XX:XX:XX:XX:XX:XX');
        input.classList.add('is-invalid');
    } else {
        input.setCustomValidity('');
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
        input.value = value; // Converter para maiúsculas
    }
}

// Função para validar endereços IP
function validateIpAddress(input) {
    const ipPattern = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    const value = input.value;
    
    if (value && !ipPattern.test(value)) {
        input.setCustomValidity('Endereço IP inválido');
        input.classList.add('is-invalid');
    } else {
        input.setCustomValidity('');
        input.classList.remove('is-invalid');
        if (value) input.classList.add('is-valid');
    }
}

// Função para copiar texto para clipboard
function copyToClipboard(text, successMessage = 'Copiado para a área de transferência!') {
    navigator.clipboard.writeText(text).then(() => {
        showAlert('success', successMessage, 2000);
    }).catch(err => {
        console.error('Erro ao copiar:', err);
        showAlert('danger', 'Erro ao copiar para a área de transferência');
    });
}

// Função para formatar endereços MAC automaticamente
function formatMacAddress(input) {
    let value = input.value.replace(/[^0-9A-Fa-f]/g, '').toUpperCase();
    
    if (value.length <= 12) {
        // Adicionar ':' a cada 2 caracteres
        value = value.replace(/(.{2})(?=.)/g, '$1:');
        input.value = value;
    }
}

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips do Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Validação de campos MAC
    const macInputs = document.querySelectorAll('input[name*="mac_address"]');
    macInputs.forEach(input => {
        input.addEventListener('input', () => formatMacAddress(input));
        input.addEventListener('blur', () => validateMacAddress(input));
    });
    
    // Validação de campos IP
    const ipInputs = document.querySelectorAll('input[name*="ip_address"], input[name*="subnet_mask"]');
    ipInputs.forEach(input => {
        input.addEventListener('blur', () => validateIpAddress(input));
    });
    
    // Adicionar classe de animação aos cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.classList.add('fade-in');
    });
    
    // Inicializar auto-refresh se habilitado
    initAutoRefresh();
    
    // Adicionar eventos de confirmação para botões de exclusão
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm-delete');
            if (!confirmDelete(message)) {
                e.preventDefault();
            }
        });
    });
    
    // Adicionar funcionalidade de duplo clique para copiar IPs e MACs
    const copyableElements = document.querySelectorAll('code, .copyable');
    copyableElements.forEach(element => {
        element.style.cursor = 'pointer';
        element.title = 'Duplo clique para copiar';
        element.addEventListener('dblclick', function() {
            copyToClipboard(this.textContent);
        });
    });
});

// Função para busca em tabelas
function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    
    if (!input || !table) return;
    
    input.addEventListener('keyup', function() {
        const filter = this.value.toLowerCase();
        const rows = table.getElementsByTagName('tr');
        
        for (let i = 1; i < rows.length; i++) { // Pular cabeçalho
            const row = rows[i];
            const cells = row.getElementsByTagName('td');
            let found = false;
            
            for (let j = 0; j < cells.length; j++) {
                if (cells[j].textContent.toLowerCase().indexOf(filter) > -1) {
                    found = true;
                    break;
                }
            }
            
            row.style.display = found ? '' : 'none';
        }
    });
}

// Função para atualizar status em tempo real
function startStatusUpdates(interval = 30000) {
    setInterval(async function() {
        const deviceRows = document.querySelectorAll('[data-device-id]');
        
        for (const row of deviceRows) {
            const deviceId = row.getAttribute('data-device-id');
            
            try {
                const response = await fetch(`/api/device-status/${deviceId}`);
                const data = await response.json();
                
                updateDeviceStatus(deviceId, data.status);
            } catch (error) {
                console.error('Erro ao atualizar status do dispositivo:', deviceId, error);
            }
        }
    }, interval);
}

// Função para mostrar loading em botões
function setButtonLoading(button, loading = true) {
    if (loading) {
        button.dataset.originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Aguarde...';
        button.disabled = true;
        button.classList.add('loading');
    } else {
        button.innerHTML = button.dataset.originalText || button.innerHTML;
        button.disabled = false;
        button.classList.remove('loading');
    }
}

// Função para envio de formulários com feedback
function submitFormWithFeedback(form, successMessage = 'Operação realizada com sucesso!') {
    const submitButton = form.querySelector('button[type="submit"]');
    
    form.addEventListener('submit', function() {
        if (submitButton) {
            setButtonLoading(submitButton, true);
        }
    });
    
    // Se houver mensagens flash, assumir que o formulário foi processado
    const alerts = document.querySelectorAll('.alert');
    if (alerts.length > 0 && submitButton) {
        setButtonLoading(submitButton, false);
    }
}

// Exportar funções para uso global
window.WOLSystem = {
    showAlert,
    confirmDelete,
    pingDevice,
    validateMacAddress,
    validateIpAddress,
    copyToClipboard,
    formatMacAddress,
    filterTable,
    startStatusUpdates,
    setButtonLoading,
    submitFormWithFeedback
};
