from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import enum

db = SQLAlchemy()

# Tabela de associação para usuários e grupos de dispositivos
user_device_groups = db.Table('user_device_groups',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('device_group_id', db.Integer, db.ForeignKey('device_group.id'), primary_key=True)
)

# Tabela de associação para dispositivos e grupos
device_group_association = db.Table('device_group_association',
    db.Column('device_id', db.Integer, db.ForeignKey('device.id'), primary_key=True),
    db.Column('device_group_id', db.Integer, db.ForeignKey('device_group.id'), primary_key=True)
)

class DeviceStatus(enum.Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    UNKNOWN = "unknown"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relacionamento com grupos de dispositivos
    device_groups = db.relationship('DeviceGroup', secondary=user_device_groups, 
                                   back_populates='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can_access_device(self, device):
        """Verifica se o usuário pode acessar um dispositivo específico"""
        if self.is_admin:
            return True
        
        # Verifica se o dispositivo está em algum grupo que o usuário tem acesso
        for group in self.device_groups:
            if device in group.devices:
                return True
        return False

    def __repr__(self):
        return f'<User {self.username}>'

class DeviceGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    users = db.relationship('User', secondary=user_device_groups, 
                           back_populates='device_groups')
    devices = db.relationship('Device', secondary=device_group_association, 
                             back_populates='groups')

    def __repr__(self):
        return f'<DeviceGroup {self.name}>'

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    network_name = db.Column(db.String(100))
    ip_address = db.Column(db.String(15), nullable=False)
    mac_address = db.Column(db.String(17), nullable=False, unique=True)
    description = db.Column(db.Text)
    status = db.Column(db.Enum(DeviceStatus), default=DeviceStatus.UNKNOWN)
    last_seen = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Configurações específicas
    wol_port = db.Column(db.Integer, default=9)
    subnet_mask = db.Column(db.String(15), default='255.255.255.0')
    enable_ping_monitoring = db.Column(db.Boolean, default=True)
    enable_network_discovery = db.Column(db.Boolean, default=True)
    
    # Relacionamentos
    groups = db.relationship('DeviceGroup', secondary=device_group_association, 
                            back_populates='devices')
    logs = db.relationship('DeviceLog', backref='device', lazy=True, 
                          cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Device {self.name} ({self.ip_address})>'

class DeviceLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)  # WOL, SHUTDOWN, PING, etc.
    status = db.Column(db.String(20), nullable=False)  # SUCCESS, FAILED, TIMEOUT
    message = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='device_logs')

    def __repr__(self):
        return f'<DeviceLog {self.action} - {self.status}>'

class SystemConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    description = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @staticmethod
    def get_config(key, default=None):
        config = SystemConfig.query.filter_by(key=key).first()
        return config.value if config else default

    @staticmethod
    def set_config(key, value, description=None):
        config = SystemConfig.query.filter_by(key=key).first()
        if config:
            config.value = value
            if description:
                config.description = description
        else:
            config = SystemConfig(key=key, value=value, description=description)
            db.session.add(config)
        db.session.commit()

    def __repr__(self):
        return f'<SystemConfig {self.key}>'
