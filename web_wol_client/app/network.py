import socket
import struct
import subprocess
import ipaddress
import platform
import nmap
import threading
import time
from datetime import datetime
from ping3 import ping
from wakeonlan import send_magic_packet
from .models import Device, DeviceLog, DeviceStatus, db
from flask import current_app

class NetworkManager:
    def __init__(self):
        self.nm = nmap.PortScanner()
        self._monitoring_active = False
        self._monitoring_thread = None

    def send_wol_packet(self, mac_address, ip_address=None, port=9):
        """Envia pacote Wake-on-LAN para um dispositivo"""
        try:
            # Remove caracteres especiais do MAC
            mac_clean = mac_address.replace(':', '').replace('-', '')
            
            # Enviar WOL packet
            if ip_address:
                send_magic_packet(mac_clean, ip_address=ip_address, port=port)
            else:
                send_magic_packet(mac_clean, port=port)
            
            return True, "Pacote WOL enviado com sucesso"
        except Exception as e:
            return False, f"Erro ao enviar WOL: {str(e)}"

    def ping_device(self, ip_address, timeout=3):
        """Verifica se um dispositivo está online via ping"""
        try:
            result = ping(ip_address, timeout=timeout)
            if result is not None and result is not False:
                return True, f"Ping bem-sucedido: {result:.2f}ms"
            else:
                return False, "Dispositivo não responde ao ping"
        except Exception as e:
            return False, f"Erro no ping: {str(e)}"

    def shutdown_device(self, ip_address, username=None, password=None):
        """Tenta desligar um dispositivo Windows remotamente"""
        try:
            if platform.system() == "Windows":
                # Comando para Windows
                cmd = f"shutdown /s /m \\\\{ip_address} /t 0"
            else:
                # Comando para Linux (via SSH seria necessário)
                return False, "Shutdown remoto não implementado para este sistema"
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                return True, "Comando de shutdown enviado"
            else:
                return False, f"Erro: {result.stderr}"
                
        except Exception as e:
            return False, f"Erro ao desligar dispositivo: {str(e)}"

    def suspend_device(self, ip_address, username=None, password=None):
        """Tenta suspender um dispositivo Windows remotamente"""
        try:
            if platform.system() == "Windows":
                # Comando para Windows
                cmd = f"rundll32.exe powrprof.dll,SetSuspendState 0,1,0"
                # Nota: Isso suspende a máquina local. Para remoto, seria necessário WMI ou SSH
                return False, "Suspend remoto requer configuração adicional"
            else:
                return False, "Suspend remoto não implementado para este sistema"
                
        except Exception as e:
            return False, f"Erro ao suspender dispositivo: {str(e)}"

    def scan_network(self, network_range="192.168.1.0/24", scan_type="ping"):
        """Escaneia a rede procurando por dispositivos ativos"""
        try:
            discovered_devices = []
            
            if scan_type == "ping":
                # Ping scan
                network = ipaddress.IPv4Network(network_range, strict=False)
                for ip in network.hosts():
                    ip_str = str(ip)
                    is_alive, response = self.ping_device(ip_str, timeout=1)
                    
                    if is_alive:
                        # Tentar obter MAC address via ARP
                        mac = self._get_mac_address(ip_str)
                        hostname = self._get_hostname(ip_str)
                        
                        discovered_devices.append({
                            'ip': ip_str,
                            'mac': mac,
                            'hostname': hostname,
                            'status': 'online'
                        })
            
            elif scan_type == "arp":
                # ARP scan usando nmap
                result = self.nm.scan(hosts=network_range, arguments='-sn')
                
                for host in self.nm.all_hosts():
                    if self.nm[host].state() == 'up':
                        mac = None
                        vendor = None
                        
                        if 'mac' in self.nm[host]['addresses']:
                            mac = self.nm[host]['addresses']['mac']
                        
                        hostname = None
                        if 'hostnames' in self.nm[host] and self.nm[host]['hostnames']:
                            hostname = self.nm[host]['hostnames'][0]['name']
                        
                        discovered_devices.append({
                            'ip': host,
                            'mac': mac,
                            'hostname': hostname,
                            'status': 'online'
                        })
            
            return True, discovered_devices
            
        except Exception as e:
            return False, f"Erro no scan de rede: {str(e)}"

    def _get_mac_address(self, ip_address):
        """Obtém o endereço MAC via ARP"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(f"arp -a {ip_address}", shell=True, 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    # Parse do resultado do ARP no Windows
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if ip_address in line:
                            parts = line.split()
                            if len(parts) >= 2:
                                return parts[1].replace('-', ':')
            else:
                result = subprocess.run(f"arp -n {ip_address}", shell=True, 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    # Parse do resultado do ARP no Linux
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if ip_address in line:
                            parts = line.split()
                            if len(parts) >= 3:
                                return parts[2]
            
            return None
        except:
            return None

    def _get_hostname(self, ip_address):
        """Obtém o hostname via DNS reverso"""
        try:
            hostname = socket.gethostbyaddr(ip_address)[0]
            return hostname
        except:
            return None

    def check_device_status(self, device):
        """Verifica o status atual de um dispositivo"""
        try:
            if device.enable_ping_monitoring:
                is_online, message = self.ping_device(device.ip_address)
                
                # Atualizar status no banco
                old_status = device.status
                device.status = DeviceStatus.ONLINE if is_online else DeviceStatus.OFFLINE
                device.last_seen = datetime.utcnow() if is_online else device.last_seen
                
                # Log da mudança de status
                if old_status != device.status:
                    log = DeviceLog(
                        device_id=device.id,
                        action='STATUS_CHECK',
                        status='SUCCESS',
                        message=f"Status mudou de {old_status.value} para {device.status.value}"
                    )
                    db.session.add(log)
                
                db.session.commit()
                return is_online, message
            else:
                return None, "Monitoramento desabilitado"
                
        except Exception as e:
            return False, f"Erro ao verificar status: {str(e)}"

    def start_monitoring(self, interval=30):
        """Inicia monitoramento automático de dispositivos"""
        if self._monitoring_active:
            return False, "Monitoramento já está ativo"
        
        self._monitoring_active = True
        self._monitoring_thread = threading.Thread(target=self._monitoring_loop, args=(interval,))
        self._monitoring_thread.daemon = True
        self._monitoring_thread.start()
        
        return True, "Monitoramento iniciado"

    def stop_monitoring(self):
        """Para o monitoramento automático"""
        self._monitoring_active = False
        if self._monitoring_thread:
            self._monitoring_thread.join()
        return True, "Monitoramento parado"

    def _monitoring_loop(self, interval):
        """Loop principal do monitoramento"""
        while self._monitoring_active:
            try:
                with current_app.app_context():
                    devices = Device.query.filter_by(enable_ping_monitoring=True).all()
                    
                    for device in devices:
                        if not self._monitoring_active:
                            break
                        
                        self.check_device_status(device)
                        time.sleep(1)  # Pequeno delay entre dispositivos
                
                # Aguardar próximo ciclo
                time.sleep(interval)
                
            except Exception as e:
                current_app.logger.error(f"Erro no monitoramento: {str(e)}")
                time.sleep(interval)

# Instância global do gerenciador de rede
network_manager = NetworkManager()
