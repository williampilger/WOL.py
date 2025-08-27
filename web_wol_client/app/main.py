import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime
import secrets

# Imports dos módulos da aplicação
from .models import db, User, Device, DeviceGroup, DeviceLog, SystemConfig, DeviceStatus
from .forms import LoginForm, UserForm, DeviceForm, DeviceGroupForm, ChangePasswordForm, NetworkScanForm, WOLForm
from .network import network_manager

def create_app():
    app = Flask(__name__)
    
    # Configurações
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(16)
    
    # Configurar caminho do banco de dados
    db_path = os.environ.get('DATABASE_PATH', os.path.join(os.getcwd(), 'data', 'wol_system.db'))
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensões
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Criar tabelas e dados iniciais
    with app.app_context():
        db.create_all()
        create_initial_data()
    
    # Iniciar monitoramento automático em background
    import atexit
    network_manager.start_monitoring(interval=60)
    
    # Parar monitoramento quando aplicação for encerrada
    atexit.register(network_manager.stop_monitoring)
    
    # Rotas de autenticação
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            
            if user and user.check_password(form.password.data) and user.is_active:
                login_user(user, remember=form.remember_me.data)
                user.last_login = datetime.utcnow()
                db.session.commit()
                
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            else:
                flash('Usuário ou senha inválidos, ou conta desativada.', 'error')
        
        return render_template('login.html', form=form)
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Logout realizado com sucesso.', 'success')
        return redirect(url_for('login'))
    
    # Rota principal
    @app.route('/')
    @login_required
    def dashboard():
        # Estatísticas gerais
        total_devices = Device.query.count()
        online_devices = Device.query.filter_by(status=DeviceStatus.ONLINE).count()
        offline_devices = Device.query.filter_by(status=DeviceStatus.OFFLINE).count()
        
        # Dispositivos acessíveis pelo usuário
        if current_user.is_admin:
            user_devices = Device.query.all()
        else:
            user_devices = []
            for group in current_user.device_groups:
                user_devices.extend(group.devices)
            user_devices = list(set(user_devices))  # Remove duplicatas
        
        # Logs recentes
        recent_logs = DeviceLog.query.order_by(DeviceLog.timestamp.desc()).limit(10).all()
        
        return render_template('dashboard.html',
                             total_devices=total_devices,
                             online_devices=online_devices,
                             offline_devices=offline_devices,
                             user_devices=user_devices,
                             recent_logs=recent_logs)
    
    # Rotas de dispositivos
    @app.route('/devices')
    @login_required
    def devices():
        if current_user.is_admin:
            devices = Device.query.all()
        else:
            devices = []
            for group in current_user.device_groups:
                devices.extend(group.devices)
            devices = list(set(devices))
        
        return render_template('devices.html', devices=devices)
    
    @app.route('/devices/add', methods=['GET', 'POST'])
    @login_required
    def add_device():
        if not current_user.is_admin:
            flash('Acesso negado. Apenas administradores podem adicionar dispositivos.', 'error')
            return redirect(url_for('devices'))
        
        form = DeviceForm()
        if form.validate_on_submit():
            device = Device(
                name=form.name.data,
                network_name=form.network_name.data,
                ip_address=form.ip_address.data,
                mac_address=form.mac_address.data.upper(),
                description=form.description.data,
                wol_port=form.wol_port.data,
                subnet_mask=form.subnet_mask.data,
                enable_ping_monitoring=form.enable_ping_monitoring.data,
                enable_network_discovery=form.enable_network_discovery.data
            )
            
            # Adicionar aos grupos selecionados
            for group_id in form.groups.data:
                group = DeviceGroup.query.get(group_id)
                if group:
                    device.groups.append(group)
            
            db.session.add(device)
            db.session.commit()
            
            flash(f'Dispositivo {device.name} adicionado com sucesso!', 'success')
            return redirect(url_for('devices'))
        
        return render_template('device_form.html', form=form, title='Adicionar Dispositivo')
    
    @app.route('/devices/<int:device_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_device(device_id):
        if not current_user.is_admin:
            flash('Acesso negado. Apenas administradores podem editar dispositivos.', 'error')
            return redirect(url_for('devices'))
            
        device = Device.query.get_or_404(device_id)
        
        form = DeviceForm(obj=device)
        if form.validate_on_submit():
            device.name = form.name.data
            device.network_name = form.network_name.data
            device.ip_address = form.ip_address.data
            device.mac_address = form.mac_address.data.upper()
            device.description = form.description.data
            device.wol_port = form.wol_port.data
            device.subnet_mask = form.subnet_mask.data
            device.enable_ping_monitoring = form.enable_ping_monitoring.data
            device.enable_network_discovery = form.enable_network_discovery.data
            
            # Atualizar grupos
            device.groups.clear()
            for group_id in form.groups.data:
                group = DeviceGroup.query.get(group_id)
                if group:
                    device.groups.append(group)
            
            db.session.commit()
            flash(f'Dispositivo {device.name} atualizado com sucesso!', 'success')
            return redirect(url_for('devices'))
        
        # Pré-selecionar grupos atuais
        form.groups.data = [g.id for g in device.groups]
        
        return render_template('device_form.html', form=form, device=device, title='Editar Dispositivo')
    
    @app.route('/devices/<int:device_id>/delete', methods=['POST'])
    @login_required
    def delete_device(device_id):
        if not current_user.is_admin:
            flash('Acesso negado. Apenas administradores podem excluir dispositivos.', 'error')
            return redirect(url_for('devices'))
        
        device = Device.query.get_or_404(device_id)
        device_name = device.name
        
        db.session.delete(device)
        db.session.commit()
        
        flash(f'Dispositivo {device_name} excluído com sucesso!', 'success')
        return redirect(url_for('devices'))
    
    # Rotas de ações WOL
    @app.route('/wol', methods=['GET', 'POST'])
    @login_required
    def wol():
        form = WOLForm(user=current_user)
        
        if form.validate_on_submit():
            results = []
            
            for device_id in form.device_ids.data:
                device = Device.query.get(device_id)
                if device and current_user.can_access_device(device):
                    success, message = network_manager.send_wol_packet(
                        device.mac_address,
                        device.ip_address,
                        device.wol_port
                    )
                    
                    # Log da ação
                    log = DeviceLog(
                        device_id=device.id,
                        action='WOL',
                        status='SUCCESS' if success else 'FAILED',
                        message=message,
                        user_id=current_user.id
                    )
                    db.session.add(log)
                    
                    results.append({
                        'device': device.name,
                        'success': success,
                        'message': message
                    })
            
            db.session.commit()
            
            # Mostrar resultados
            for result in results:
                status = 'success' if result['success'] else 'error'
                flash(f"{result['device']}: {result['message']}", status)
            
            return redirect(url_for('dashboard'))
        
        return render_template('wol.html', form=form)
    
    @app.route('/api/ping/<int:device_id>')
    @login_required
    def ping_device(device_id):
        device = Device.query.get_or_404(device_id)
        
        if not current_user.can_access_device(device):
            return jsonify({'error': 'Acesso negado'}), 403
        
        success, message = network_manager.ping_device(device.ip_address)
        
        # Atualizar status no banco de dados
        old_status = device.status
        device.status = DeviceStatus.ONLINE if success else DeviceStatus.OFFLINE
        device.last_seen = datetime.utcnow() if success else device.last_seen
        
        # Log da ação
        log = DeviceLog(
            device_id=device.id,
            action='PING',
            status='SUCCESS' if success else 'FAILED',
            message=message,
            user_id=current_user.id
        )
        db.session.add(log)
        
        # Log da mudança de status se houver
        if old_status != device.status:
            status_log = DeviceLog(
                device_id=device.id,
                action='STATUS_CHANGE',
                status='SUCCESS',
                message=f"Status alterado de {old_status.value} para {device.status.value} via ping manual",
                user_id=current_user.id
            )
            db.session.add(status_log)
        
        db.session.commit()
        
        return jsonify({
            'success': success,
            'message': message,
            'status': 'online' if success else 'offline',
            'device_status': device.status.value
        })
    
    @app.route('/api/refresh-all-status')
    @login_required
    def refresh_all_status():
        """Atualiza o status de todos os dispositivos manualmente"""
        try:
            devices = Device.query.all()
            accessible_devices = [d for d in devices if current_user.can_access_device(d)]
            
            updated_count = 0
            results = []
            
            for device in accessible_devices:
                if device.ip_address:
                    success, message = network_manager.ping_device(device.ip_address)
                    
                    # Atualizar status
                    old_status = device.status
                    device.status = DeviceStatus.ONLINE if success else DeviceStatus.OFFLINE
                    device.last_seen = datetime.utcnow() if success else device.last_seen
                    
                    if old_status != device.status:
                        updated_count += 1
                        
                        # Log da mudança
                        log = DeviceLog(
                            device_id=device.id,
                            action='STATUS_REFRESH',
                            status='SUCCESS',
                            message=f"Status atualizado: {old_status.value} → {device.status.value}",
                            user_id=current_user.id
                        )
                        db.session.add(log)
                    
                    results.append({
                        'device': device.name,
                        'status': device.status.value,
                        'success': success,
                        'changed': old_status != device.status
                    })
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': f'Status atualizado para {len(accessible_devices)} dispositivos. {updated_count} alterações detectadas.',
                'updated_count': updated_count,
                'total_devices': len(accessible_devices),
                'results': results
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Erro ao atualizar status: {str(e)}'
            }), 500
    
    # Rotas de usuários (apenas admin)
    @app.route('/users')
    @login_required
    def users():
        if not current_user.is_admin:
            flash('Acesso negado. Apenas administradores podem gerenciar usuários.', 'error')
            return redirect(url_for('dashboard'))
        
        users = User.query.all()
        return render_template('users.html', users=users)
    
    @app.route('/users/add', methods=['GET', 'POST'])
    @login_required
    def add_user():
        if not current_user.is_admin:
            flash('Acesso negado.', 'error')
            return redirect(url_for('dashboard'))
        
        form = UserForm()
        if form.validate_on_submit():
            # Verificar se usuário já existe
            existing_user = User.query.filter(
                (User.username == form.username.data) | 
                (User.email == form.email.data)
            ).first()
            
            if existing_user:
                flash('Usuário ou email já existe.', 'error')
                return render_template('user_form.html', form=form, title='Adicionar Usuário')
            
            user = User(
                username=form.username.data,
                email=form.email.data,
                is_admin=form.is_admin.data,
                is_active=form.is_active.data
            )
            
            if form.password.data:
                user.set_password(form.password.data)
            else:
                user.set_password('123456')  # Senha padrão
                flash('Senha padrão definida: 123456', 'warning')
            
            # Adicionar aos grupos selecionados
            for group_id in form.device_groups.data:
                group = DeviceGroup.query.get(group_id)
                if group:
                    user.device_groups.append(group)
            
            db.session.add(user)
            db.session.commit()
            
            flash(f'Usuário {user.username} criado com sucesso!', 'success')
            return redirect(url_for('users'))
        
        return render_template('user_form.html', form=form, title='Adicionar Usuário')
    
    @app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_user(user_id):
        if not current_user.is_admin:
            flash('Acesso negado.', 'error')
            return redirect(url_for('dashboard'))
        
        user = User.query.get_or_404(user_id)
        form = UserForm(obj=user)
        
        if form.validate_on_submit():
            # Verificar se username/email já existem (exceto para o usuário atual)
            existing_user = User.query.filter(
                ((User.username == form.username.data) | (User.email == form.email.data)) &
                (User.id != user.id)
            ).first()
            
            if existing_user:
                flash('Usuário ou email já existe.', 'error')
                return render_template('user_form.html', form=form, user=user, title='Editar Usuário')
            
            user.username = form.username.data
            user.email = form.email.data
            user.is_admin = form.is_admin.data
            user.is_active = form.is_active.data
            
            # Atualizar senha se fornecida
            if form.password.data:
                user.set_password(form.password.data)
                flash('Senha atualizada.', 'info')
            
            # Atualizar grupos
            user.device_groups.clear()
            for group_id in form.device_groups.data:
                group = DeviceGroup.query.get(group_id)
                if group:
                    user.device_groups.append(group)
            
            db.session.commit()
            flash(f'Usuário {user.username} atualizado com sucesso!', 'success')
            return redirect(url_for('users'))
        
        # Pré-selecionar grupos atuais
        form.device_groups.data = [g.id for g in user.device_groups]
        
        return render_template('user_form.html', form=form, user=user, title='Editar Usuário')
    
    @app.route('/users/<int:user_id>/delete', methods=['POST'])
    @login_required
    def delete_user(user_id):
        if not current_user.is_admin:
            flash('Acesso negado.', 'error')
            return redirect(url_for('dashboard'))
        
        user = User.query.get_or_404(user_id)
        
        # Não permitir exclusão do próprio usuário
        if user.id == current_user.id:
            flash('Você não pode excluir sua própria conta.', 'error')
            return redirect(url_for('users'))
        
        username = user.username
        db.session.delete(user)
        db.session.commit()
        
        flash(f'Usuário {username} excluído com sucesso!', 'success')
        return redirect(url_for('users'))
    
    @app.route('/users/<int:user_id>/toggle-status', methods=['POST'])
    @login_required
    def toggle_user_status(user_id):
        if not current_user.is_admin:
            return jsonify({'success': False, 'message': 'Acesso negado'}), 403
        
        user = User.query.get_or_404(user_id)
        
        # Não permitir desativar o próprio usuário
        if user.id == current_user.id:
            return jsonify({'success': False, 'message': 'Você não pode alterar o status da sua própria conta'}), 400
        
        user.is_active = not user.is_active
        db.session.commit()
        
        status = 'ativado' if user.is_active else 'desativado'
        return jsonify({'success': True, 'message': f'Usuário {user.username} {status} com sucesso!'})
    
    @app.route('/users/<int:user_id>/reset-password', methods=['POST'])
    @login_required
    def reset_user_password(user_id):
        if not current_user.is_admin:
            return jsonify({'success': False, 'message': 'Acesso negado'}), 403
        
        user = User.query.get_or_404(user_id)
        user.set_password('123456')  # Senha padrão
        db.session.commit()
        
        return jsonify({'success': True, 'message': f'Senha do usuário {user.username} resetada para: 123456'})
    
    # Rota para alterar senha
    @app.route('/change-password', methods=['GET', 'POST'])
    @login_required
    def change_password():
        form = ChangePasswordForm()
        
        if form.validate_on_submit():
            if current_user.check_password(form.current_password.data):
                current_user.set_password(form.new_password.data)
                db.session.commit()
                flash('Senha alterada com sucesso!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Senha atual incorreta.', 'error')
        
        return render_template('change_password.html', form=form)
    
    # Rotas de grupos
    @app.route('/groups')
    @login_required
    def groups():
        if not current_user.is_admin:
            flash('Acesso negado.', 'error')
            return redirect(url_for('dashboard'))
        
        groups = DeviceGroup.query.all()
        return render_template('groups.html', groups=groups)
    
    @app.route('/groups/add', methods=['GET', 'POST'])
    @login_required
    def add_group():
        if not current_user.is_admin:
            flash('Acesso negado.', 'error')
            return redirect(url_for('dashboard'))
        
        form = DeviceGroupForm()
        if form.validate_on_submit():
            group = DeviceGroup(
                name=form.name.data,
                description=form.description.data
            )
            
            db.session.add(group)
            db.session.commit()
            
            flash(f'Grupo {group.name} criado com sucesso!', 'success')
            return redirect(url_for('groups'))
        
        return render_template('group_form.html', form=form, title='Adicionar Grupo')
    
    @app.route('/groups/edit/<int:id>', methods=['GET', 'POST'])
    @login_required
    def edit_group(id):
        if not current_user.is_admin:
            flash('Acesso negado.', 'error')
            return redirect(url_for('dashboard'))
        
        group = DeviceGroup.query.get_or_404(id)
        
        form = DeviceGroupForm(obj=group)
        if form.validate_on_submit():
            group.name = form.name.data
            group.description = form.description.data
            
            db.session.commit()
            
            flash(f'Grupo {group.name} atualizado com sucesso!', 'success')
            return redirect(url_for('groups'))
        
        return render_template('group_form.html', form=form, title='Editar Grupo', group=group)
    
    @app.route('/groups/delete/<int:id>', methods=['POST'])
    @login_required
    def delete_group(id):
        if not current_user.is_admin:
            flash('Acesso negado.', 'error')
            return redirect(url_for('dashboard'))
        
        group = DeviceGroup.query.get_or_404(id)
        
        # Verificar se há dispositivos neste grupo
        if group.devices:
            flash(f'Não é possível excluir o grupo "{group.name}" pois há dispositivos associados.', 'error')
            return redirect(url_for('groups'))
        
        # Verificar se há usuários neste grupo
        if group.users:
            flash(f'Não é possível excluir o grupo "{group.name}" pois há usuários associados.', 'error')
            return redirect(url_for('groups'))
        
        group_name = group.name
        db.session.delete(group)
        db.session.commit()
        
        flash(f'Grupo "{group_name}" excluído com sucesso!', 'success')
        return redirect(url_for('groups'))
    
    # Rota de scan de rede
    @app.route('/network-scan', methods=['GET', 'POST'])
    @login_required
    def network_scan():
        if not current_user.is_admin:
            flash('Acesso negado.', 'error')
            return redirect(url_for('dashboard'))
        
        form = NetworkScanForm()
        results = []
        
        if form.validate_on_submit():
            success, scan_results = network_manager.scan_network(
                form.network_range.data,
                form.scan_type.data
            )
            
            if success:
                results = scan_results
                flash(f'Scan concluído. {len(results)} dispositivos encontrados.', 'success')
            else:
                flash(f'Erro no scan: {scan_results}', 'error')
        
        return render_template('network_scan.html', form=form, results=results)
    
    return app

def create_initial_data():
    """Cria dados iniciais se não existirem"""
    # Verificar se já existe usuário admin
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@localhost',
            is_admin=True,
            is_active=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Criar grupo padrão
        default_group = DeviceGroup(
            name='Todos os Dispositivos',
            description='Grupo padrão com acesso a todos os dispositivos'
        )
        db.session.add(default_group)
        
        db.session.commit()
        print("Usuário admin criado com sucesso!")
        print("Login: admin | Senha: admin123")

if __name__ == '__main__':
    app = create_app()
    
    # Iniciar monitoramento em background
    network_manager.start_monitoring(interval=60)
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    finally:
        network_manager.stop_monitoring()
