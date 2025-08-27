from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField, IntegerField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Email, Length, IPAddress, NumberRange, Optional, ValidationError
from wtforms.widgets import CheckboxInput, ListWidget
from .models import User, DeviceGroup, Device

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar-me')

class UserForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Senha', validators=[Optional(), Length(min=6, max=128)])
    is_admin = BooleanField('Administrador')
    is_active = BooleanField('Ativo', default=True)
    device_groups = SelectMultipleField('Grupos de Dispositivos', coerce=int)
    submit = SubmitField('Salvar')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.device_groups.choices = [(g.id, g.name) for g in DeviceGroup.query.all()]

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Senha Atual', validators=[DataRequired()])
    new_password = PasswordField('Nova Senha', validators=[DataRequired(), Length(min=6, max=128)])
    confirm_password = PasswordField('Confirmar Nova Senha', validators=[DataRequired()])
    submit = SubmitField('Alterar Senha')

    def validate_confirm_password(self, field):
        if field.data != self.new_password.data:
            raise ValidationError('As senhas não coincidem.')

class DeviceGroupForm(FlaskForm):
    name = StringField('Nome do Grupo', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Descrição', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Salvar')

class DeviceForm(FlaskForm):
    name = StringField('Nome do Dispositivo', validators=[DataRequired(), Length(min=2, max=100)])
    network_name = StringField('Nome de Rede', validators=[Optional(), Length(max=100)])
    ip_address = StringField('Endereço IP', validators=[DataRequired(), IPAddress()])
    mac_address = StringField('Endereço MAC', validators=[DataRequired(), Length(min=17, max=17)])
    description = TextAreaField('Descrição', validators=[Optional(), Length(max=500)])
    wol_port = IntegerField('Porta WOL', validators=[Optional(), NumberRange(min=1, max=65535)], default=9)
    subnet_mask = StringField('Máscara de Sub-rede', validators=[Optional(), IPAddress()], default='255.255.255.0')
    enable_ping_monitoring = BooleanField('Monitoramento por Ping', default=True)
    enable_network_discovery = BooleanField('Descoberta de Rede', default=True)
    groups = SelectMultipleField('Grupos', coerce=int)
    submit = SubmitField('Salvar')

    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        self.groups.choices = [(g.id, g.name) for g in DeviceGroup.query.all()]

    def validate_mac_address(self, field):
        import re
        # Validar formato MAC address (XX:XX:XX:XX:XX:XX)
        mac_pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
        if not re.match(mac_pattern, field.data):
            raise ValidationError('Formato de MAC address inválido. Use XX:XX:XX:XX:XX:XX')

class NetworkScanForm(FlaskForm):
    network_range = StringField('Faixa de Rede', 
                               validators=[DataRequired()], 
                               default='192.168.1.0/24',
                               description='Ex: 192.168.1.0/24')
    scan_type = SelectField('Tipo de Scan', 
                           choices=[('ping', 'Ping Scan'), ('arp', 'ARP Scan')],
                           default='ping')
    submit = SubmitField('Escanear')

class WOLForm(FlaskForm):
    device_ids = SelectMultipleField('Dispositivos', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Enviar WOL')

    def __init__(self, user=None, *args, **kwargs):
        super(WOLForm, self).__init__(*args, **kwargs)
        if user:
            if user.is_admin:
                devices = Device.query.all()
            else:
                # Usuários não-admin só veem dispositivos dos seus grupos
                devices = []
                for group in user.device_groups:
                    devices.extend(group.devices)
                # Remove duplicatas
                devices = list(set(devices))
            
            self.device_ids.choices = [(d.id, f"{d.name} ({d.ip_address})") for d in devices]
