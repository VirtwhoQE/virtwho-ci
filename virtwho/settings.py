import os, sys
from configparser import ConfigParser

def get_exported_param(name):
    value = os.getenv(name)
    if value is None or value == '':
        value = None
    return value

class ReaderConf(object):
    def __init__(self, path):
        self.config_parser = ConfigParser()
        try:
            with open(path) as handler:
                self.config_parser.readfp(handler)
                if sys.version_info[0] < 3:
                    self.config_parser.readfp(handler)
                else:
                    self.config_parser.read_file(handler)
        except:
            pass

    def get(self, section, option, default=None):
        try:
            value = self.config_parser.get(section, option)
        except:
            value = None
        return value

    def has_section(self, section):
        return self.config_parser.has_section(section)

class FeatureSettings(object):
    def read(self, reader):
        raise NotImplementedError('Subclasses must implement read method.')

    def validate(self):
        raise NotImplementedError('Subclasses must implement validate method.')

class Settings(object):
    def __init__(self):
        self.configured = False

    def configure(self, settings_file):
        settings_path = os.path.join(os.path.realpath(os.path.join(
            os.path.dirname(__file__),
            os.pardir)),
            settings_file)
    
        self.reader = ReaderConf(settings_path)
        attrs = map(
            lambda attr_name: (attr_name, getattr(self, attr_name)),
            dir(self)
        )
        feature_settings = filter(
            lambda tpl: isinstance(tpl[1], FeatureSettings),
            attrs
        )
        for name, settings in feature_settings:
            if self.reader.has_section(name):
                settings.read(self.reader)

        self.configured = True

class SetTrigger(FeatureSettings):
    def __init__(self, *args, **kwargs):
        super(SetTrigger, self).__init__(*args, **kwargs)
        self.type = None
        self.level = None
        self.rhel_compose = None
        self.hypervisor_list = None
        self.register_list = None
        self.rhev_iso = None
        self.errata_package = None
        self.virtwho_upstream = None
        self.arch_type = None

    def read(self, reader):
        self.type = get_exported_param("TRIGGER_TYPE")
        self.level = get_exported_param("TRIGGER_LEVEL")
        self.rhel_compose = get_exported_param("RHEL_COMPOSE")
        self.hypervisor_list = get_exported_param("HYPERVISOR_LIST")
        self.register_list = get_exported_param("REGISTER_LIST")
        self.rhev_iso = get_exported_param("RHEV_ISO")
        self.errata_package = get_exported_param("VIRTWHO_ERRATA_PACKAGE")
        self.virtwho_upstream = get_exported_param("VIRTWHO_UPSTREAM")
        self.arch_type = get_exported_param("ARCH_TYPE")
        if not self.type:
            self.type = reader.get('trigger', 'type')
        if not self.level:
            self.level = reader.get('trigger', 'level')
        if not self.rhel_compose:
            self.rhel_compose = reader.get('trigger', 'rhel_compose')
        if not self.hypervisor_list:
            self.hypervisor_list = reader.get('trigger', 'hypervisor_list')
        if not self.register_list:
            self.register_list = reader.get('trigger', 'register_list')
        if not self.rhev_iso:
            self.rhev_iso = reader.get('trigger', 'rhev_iso')
        if not self.errata_package:
            self.errata_package = reader.get('trigger', 'errata_package')
        if not self.virtwho_upstream:
            self.virtwho_upstream = reader.get('trigger', 'virtwho_upstream')
        if not self.arch_type:
            self.arch_type = reader.get('trigger', 'arch_type')

class SetRepo(FeatureSettings):
    def __init__(self, *args, **kwargs):
        super(SetRepo, self).__init__(*args, **kwargs)
        self.rhel = None
        self.rhel_update = None
        self.rhel_brew = None
        self.rhel_sat = None
        self.epel = None

    def read(self, reader):
        self.rhel = reader.get('repo', 'rhel')
        self.rhel_update = reader.get('repo', 'rhel_update')
        self.rhel_brew = reader.get('repo', 'rhel_brew')
        self.rhel_sat = reader.get('repo', 'rhel_sat')
        self.epel = reader.get('repo', 'epel')

class SetJenkins(FeatureSettings):
    def __init__(self, *args, **kwargs):
        super(SetJenkins, self).__init__(*args, **kwargs)
        self.url = None
        self.username = None
        self.password = None

    def read(self, reader):
        self.url = reader.get('jenkins', 'url')
        self.username = reader.get('jenkins', 'username')
        self.password = reader.get('jenkins', 'password')

class SetDocker(FeatureSettings):
    def __init__(self, *args, **kwargs):
        super(SetDocker, self).__init__(*args, **kwargs)
        self.server = None
        self.server_user = None
        self.server_passwd = None
        self.slave = None
        self.slave_user = None
        self.slave_passwd = None
        self.container_user = None
        self.container_passwd = None

    def read(self, reader):
        self.server = reader.get('docker', 'server')
        self.server_user = reader.get('docker', 'server_user')
        self.server_passwd = reader.get('docker', 'server_passwd')
        self.slave = reader.get('docker', 'slave')
        self.slave_user = reader.get('docker', 'slave_user')
        self.slave_passwd = reader.get('docker', 'slave_passwd')
        self.container_user = reader.get('docker', 'container_user')
        self.container_passwd = reader.get('docker', 'container_passwd')

class SetBeaker(FeatureSettings):
    def __init__(self, *args, **kwargs):
        super(SetBeaker, self).__init__(*args, **kwargs)
        self.client = None
        self.client_user = None
        self.client_passwd = None
        self.default_user = None
        self.default_passwd = None
        self.keytab = None
        self.principal = None

    def read(self, reader):
        self.client = reader.get('beaker', 'client')
        self.client_user = reader.get('beaker', 'client_user')
        self.client_passwd = reader.get('beaker', 'client_passwd')
        self.default_user = reader.get('beaker', 'default_user')
        self.default_passwd = reader.get('beaker', 'default_passwd')
        self.keytab = reader.get('beaker', 'keytab')
        self.principal = reader.get('beaker', 'principal')

class SetPolarion(FeatureSettings):
    def __init__(self, *args, **kwargs):
        super(SetPolarion, self).__init__(*args, **kwargs)
        self.url = None
        self.username = None
        self.password = None

    def read(self, reader):
        self.url = reader.get('polarion', 'url')
        self.username = reader.get('polarion', 'username')
        self.password = reader.get('polarion', 'password')

class SetNFS(FeatureSettings):
    def __init__(self, *args, **kwargs):
        super(SetNFS, self).__init__(*args, **kwargs)
        self.server = None
        self.server_user = None
        self.server_passwd = None
        self.rhel_mount = None
        self.rhel_url = None
        self.rhev_mount = None
        self.rhev_url = None

    def read(self, reader):
        self.server = reader.get('nfs', 'server')
        self.server_user = reader.get('nfs', 'server_user')
        self.server_passwd = reader.get('nfs', 'server_passwd')
        self.rhel_mount = reader.get('nfs', 'rhel_mount')
        self.rhel_url = reader.get('nfs', 'rhel_url')
        self.rhev_mount = reader.get('nfs', 'rhev_mount')
        self.rhev_url = reader.get('nfs', 'rhev_url')

class SetRegister(FeatureSettings):
    def __init__(self, *args, **kwargs):
        super(SetRegister, self).__init__(*args, **kwargs)
        self.serverurl = None
        self.baseurl = None
        self.username = None
        self.password = None
        self.employee_sku = None

    def read(self, reader):
        self.serverurl = reader.get('register', 'serverurl')
        self.baseurl = reader.get('register', 'baseurl')
        self.username = reader.get('register', 'username')
        self.password = reader.get('register', 'password')
        self.employee_sku = reader.get('register', 'employee_sku')

class SetStage(FeatureSettings):
    def __init__(self, *args, **kwargs):
        super(SetStage, self).__init__(*args, **kwargs)
        self.server = None
        self.esx_user = None
        self.esx_passwd = None
        self.esx_org = None
        self.xen_user = None
        self.xen_passwd = None
        self.xen_org = None
        self.hyperv_user = None
        self.hyperv_passwd = None
        self.hyperv_org = None
        self.rhevm_user = None
        self.rhevm_passwd = None
        self.rhevm_org = None
        self.vdsm_user = None
        self.vdsm_passwd = None
        self.vdsm_org = None
        self.libvirt_remote_user = None
        self.libvirt_remote_passwd = None
        self.libvirt_remote_org = None
        self.libvirt_local_user = None
        self.libvirt_local_passwd = None
        self.libvirt_local_org = None

    def read(self, reader):
        self.server = reader.get('stage', 'server')
        self.esx_user = reader.get('stage', 'esx_user')
        self.esx_passwd = reader.get('stage', 'esx_passwd')
        self.esx_org = reader.get('stage', 'esx_org')
        self.xen_user = reader.get('stage', 'xen_user')
        self.xen_passwd = reader.get('stage', 'xen_passwd')
        self.xen_org = reader.get('stage', 'xen_org')
        self.hyperv_user = reader.get('stage', 'hyperv_user')
        self.hyperv_passwd = reader.get('stage', 'hyperv_passwd')
        self.hyperv_org = reader.get('stage', 'hyperv_org')
        self.rhevm_user = reader.get('stage', 'rhevm_user')
        self.rhevm_passwd = reader.get('stage', 'rhevm_passwd')
        self.rhevm_org = reader.get('stage', 'rhevm_org')
        self.vdsm_user = reader.get('stage', 'vdsm_user')
        self.vdsm_passwd = reader.get('stage', 'vdsm_passwd')
        self.vdsm_org = reader.get('stage', 'vdsm_org')
        self.libvirt_remote_user = reader.get('stage', 'libvirt_remote_user')
        self.libvirt_remote_passwd = reader.get('stage', 'libvirt_remote_passwd')
        self.libvirt_remote_org = reader.get('stage', 'libvirt_remote_org')
        self.libvirt_local_user = reader.get('stage', 'libvirt_local_user')
        self.libvirt_local_passwd = reader.get('stage', 'libvirt_local_passwd')
        self.libvirt_local_org = reader.get('stage', 'libvirt_local_org')

class SetSatellite(FeatureSettings):
    def __init__(self, *args, **kwargs):
        super(SetSatellite, self).__init__(*args, **kwargs)
        self.admin_user = None
        self.admin_passwd = None
        self.default_org = None
        self.default_env = None
        self.extra_org = None
        self.rhel6_compose = None
        self.rhel7_compose = None
        self.rhel8_compose = None
        self.manifest = None
        self.activation_key = None

    def read(self, reader):
        self.admin_user = reader.get('satellite', 'admin_user')
        self.admin_passwd = reader.get('satellite', 'admin_passwd')
        self.default_org = reader.get('satellite', 'default_org')
        self.default_env = reader.get('satellite', 'default_env')
        self.extra_org = reader.get('satellite', 'extra_org')
        self.rhel6_compose = reader.get('satellite', 'rhel6_compose')
        self.rhel7_compose = reader.get('satellite', 'rhel7_compose')
        self.rhel8_compose = reader.get('satellite', 'rhel8_compose')
        self.manifest = reader.get('satellite', 'manifest')
        self.activation_key = reader.get('satellite', 'activation_key')

class SetVcenter(FeatureSettings):
    def __init__(self, *args, **kwargs):
        super(SetVcenter, self).__init__(*args, **kwargs)
        self.ip = None
        self.admin_user = None
        self.admin_passwd = None
        self.ssh_user = None
        self.ssh_passwd = None
        self.master = None
        self.master_user = None
        self.master_passwd = None
        self.slave = None
        self.slave_user = None
        self.slave_passwd = None
        self.guest_name = None
        self.guest_user = None
        self.guest_passwd = None
        self.image_path = None

    def read(self, reader):
        self.ip = reader.get('vcenter', 'ip')
        self.admin_user = reader.get('vcenter', 'admin_user')
        self.admin_passwd = reader.get('vcenter', 'admin_passwd') 
        self.ssh_user = reader.get('vcenter', 'ssh_user') 
        self.ssh_passwd = reader.get('vcenter', 'ssh_passwd')
        self.master = reader.get('vcenter', 'master')
        self.master_user = reader.get('vcenter', 'master_user')
        self.master_passwd = reader.get('vcenter', 'master_passwd')
        self.slave = reader.get('vcenter', 'slave')
        self.slave_user = reader.get('vcenter', 'slave_user')
        self.slave_passwd = reader.get('vcenter', 'slave_passwd')
        self.guest_name = reader.get('vcenter', 'guest_name')
        self.guest_user = reader.get('vcenter', 'guest_user')
        self.guest_passwd = reader.get('vcenter', 'guest_passwd')
        self.image_path = reader.get('vcenter', 'image_path')

class SetXen(FeatureSettings):
    def __init__(self, *args, **kwargs):
        super(SetXen, self).__init__(*args, **kwargs)
        self.master = None
        self.master_user = None
        self.master_passwd = None
        self.slave = None
        self.slave_user = None
        self.slave_passwd = None
        self.guest_name = None
        self.guest_user = None
        self.guest_passwd = None
        self.sr_name = None
        self.sr_server = None
        self.sr_path = None
        self.image_path = None

    def read(self, reader):
        self.master = reader.get('xen', 'master') 
        self.master_user = reader.get('xen', 'master_user') 
        self.master_passwd = reader.get('xen', 'master_passwd')
        self.slave = reader.get('xen', 'slave')
        self.slave_user = reader.get('xen', 'slave_user')
        self.slave_passwd = reader.get('xen', 'slave_passwd')
        self.guest_name = reader.get('xen', 'guest_name')
        self.guest_user = reader.get('xen', 'guest_user')
        self.guest_passwd = reader.get('xen', 'guest_passwd')
        self.sr_name = reader.get('xen', 'sr_name')
        self.sr_server = reader.get('xen', 'sr_server')
        self.sr_path = reader.get('xen', 'sr_path')
        self.image_path = reader.get('xen', 'image_path')

class SetHyperv(FeatureSettings):
    def __init__(self, *args, **kwargs):
        super(SetHyperv, self).__init__(*args, **kwargs)
        self.master = None
        self.master_user = None
        self.master_passwd = None
        self.guest_name = None
        self.guest_user = None
        self.guest_passwd = None
        self.image_path = None

    def read(self, reader):
        self.master = reader.get('hyperv', 'master') 
        self.master_user = reader.get('hyperv', 'master_user') 
        self.master_passwd = reader.get('hyperv', 'master_passwd')
        self.guest_name = reader.get('hyperv', 'guest_name')
        self.guest_user = reader.get('hyperv', 'guest_user')
        self.guest_passwd = reader.get('hyperv', 'guest_passwd')
        self.image_path = reader.get('hyperv', 'image_path')

class SetRHEVM(FeatureSettings):
    def __init__(self, *args, **kwargs):
        super(SetRHEVM, self).__init__(*args, **kwargs)
        self.rhevm_ip = None
        self.rhevm_ssh_user = None
        self.rhevm_ssh_passwd = None
        self.rhevm_admin_user = None
        self.rhevm_admin_passwd = None
        self.master = None
        self.master_user = None
        self.master_passwd = None
        self.slave = None
        self.slave_user = None
        self.slave_passwd = None
        self.datacenter = None
        self.cluster = None
        self.cputype = None
        self.storage = None
        self.guest_name = None
        self.guest_user = None
        self.guest_passwd = None
        self.template = None
        self.disk = None
        self.nfs_path = None

    def read(self, reader):
        self.rhevm_ip = reader.get('rhevm', 'rhevm_ip') 
        self.rhevm_ssh_user = reader.get('rhevm', 'rhevm_ssh_user') 
        self.rhevm_ssh_passwd = reader.get('rhevm', 'rhevm_ssh_passwd') 
        self.rhevm_admin_user = reader.get('rhevm', 'rhevm_admin_user')
        self.rhevm_admin_passwd = reader.get('rhevm', 'rhevm_admin_passwd')
        self.master = reader.get('rhevm', 'master')
        self.master_user = reader.get('rhevm', 'master_user')
        self.master_passwd = reader.get('rhevm', 'master_passwd')
        self.slave = reader.get('rhevm', 'slave')
        self.slave_user = reader.get('rhevm', 'slave_user')
        self.slave_passwd = reader.get('rhevm', 'slave_passwd')
        self.datacenter = reader.get('rhevm', 'datacenter')
        self.cluster = reader.get('rhevm', 'cluster')
        self.cputype = reader.get('rhevm', 'cputype')
        self.storage = reader.get('rhevm', 'storage')
        self.guest_name = reader.get('rhevm', 'guest_name')
        self.guest_user = reader.get('rhevm', 'guest_user')
        self.guest_passwd = reader.get('rhevm', 'guest_passwd')
        self.template = reader.get('rhevm', 'template')
        self.disk = reader.get('rhevm', 'disk')
        self.nfs_path = reader.get('rhevm', 'nfs_path')

class SetVDSM(FeatureSettings):
    def __init__(self, *args, **kwargs):
        super(SetVDSM, self).__init__(*args, **kwargs)
        self.rhevm_ip = None
        self.rhevm_ssh_user = None
        self.rhevm_ssh_passwd = None
        self.rhevm_admin_user = None
        self.rhevm_admin_passwd = None
        self.master = None
        self.master_user = None
        self.master_passwd = None
        self.datacenter = None
        self.cluster = None
        self.cputype = None
        self.storage = None
        self.guest_name = None
        self.guest_user = None
        self.guest_passwd = None
        self.template = None
        self.disk = None
        self.nfs_path = None

    def read(self, reader):
        self.rhevm_ip = reader.get('vdsm', 'rhevm_ip') 
        self.rhevm_ssh_user = reader.get('vdsm', 'rhevm_ssh_user') 
        self.rhevm_ssh_passwd = reader.get('vdsm', 'rhevm_ssh_passwd') 
        self.rhevm_admin_user = reader.get('vdsm', 'rhevm_admin_user')
        self.rhevm_admin_passwd = reader.get('vdsm', 'rhevm_admin_passwd')
        self.master = reader.get('vdsm', 'master')
        self.master_user = reader.get('vdsm', 'master_user')
        self.master_passwd = reader.get('vdsm', 'master_passwd')
        self.datacenter = reader.get('vdsm', 'datacenter')
        self.cluster = reader.get('vdsm', 'cluster')
        self.cputype = reader.get('vdsm', 'cputype')
        self.storage = reader.get('vdsm', 'storage')
        self.guest_name = reader.get('vdsm', 'guest_name')
        self.guest_user = reader.get('vdsm', 'guest_user')
        self.guest_passwd = reader.get('vdsm', 'guest_passwd')
        self.template = reader.get('vdsm', 'template')
        self.disk = reader.get('vdsm', 'disk')
        self.nfs_path = reader.get('vdsm', 'nfs_path')

class SetLibvirt(FeatureSettings):
    def __init__(self, *args, **kwargs):
        super(SetLibvirt, self).__init__(*args, **kwargs)
        self.remote = None
        self.remote_user = None
        self.remote_passwd = None
        self.local = None
        self.local_user = None
        self.local_passwd = None
        self.guest_name = None
        self.guest_user = None
        self.guest_passwd = None
        self.image_path = None
        self.image_url = None
        self.xml_path = None
        self.xml_url = None

    def read(self, reader):
        self.remote = reader.get('libvirt', 'remote')
        self.remote_user = reader.get('libvirt', 'remote_user')
        self.remote_passwd = reader.get('libvirt', 'remote_passwd')
        self.local = reader.get('libvirt', 'local')
        self.local_user = reader.get('libvirt', 'local_user')
        self.local_passwd = reader.get('libvirt', 'local_passwd')
        self.guest_name = reader.get('libvirt', 'guest_name')
        self.guest_user = reader.get('libvirt', 'guest_user')
        self.guest_passwd = reader.get('libvirt', 'guest_passwd')
        self.image_path = reader.get('libvirt', 'image_path')
        self.image_url = reader.get('libvirt', 'image_url')
        self.xml_path = reader.get('libvirt', 'xml_path')
        self.xml_url = reader.get('libvirt', 'xml_url')

class DeploySettings(Settings):
    def __init__(self):
        self.trigger = SetTrigger()
        self.repo = SetRepo()
        self.jenkins = SetJenkins()
        self.docker = SetDocker()
        self.beaker = SetBeaker()
        self.polarion = SetPolarion()
        self.nfs = SetNFS()
        self.register = SetRegister()
        self.stage = SetStage()
        self.satellite = SetSatellite()
        self.vcenter = SetVcenter()
        self.xen = SetXen()
        self.hyperv = SetHyperv()
        self.rhevm = SetRHEVM()
        self.vdsm = SetVDSM()
        self.libvirt = SetLibvirt()

class ConfigureVirtwho(FeatureSettings):
    def __init__(self, *args, **kwargs):
        super(ConfigureVirtwho, self).__init__(*args, **kwargs)
        self.trigger_type = None
        self.rhel_compose = None
        self.host_ip = None
        self.host_user = None
        self.host_passwd = None

    def read(self, reader):
        self.trigger_type = get_exported_param("TRIGGER_TYPE")
        self.rhel_compose = get_exported_param("RHEL_COMPOSE")
        self.host_ip = get_exported_param("VIRTWHO_HOST_IP")
        self.host_user = get_exported_param("VIRTWHO_HOST_USER")
        self.host_passwd = get_exported_param("VIRTWHO_HOST_PASSWD")
        if not self.trigger_type:
            self.trigger_type = reader.get('virtwho', 'trigger_type')
        if not self.rhel_compose:
            self.rhel_compose = reader.get('virtwho', 'rhel_compose')
        if not self.host_ip:
            self.host_ip = reader.get('virtwho', 'host_ip')
        if not self.host_user:
            self.host_user = reader.get('virtwho', 'host_user')
        if not self.host_passwd:
            self.host_passwd = reader.get('virtwho', 'host_passwd')

class ConfigureHypervisor(FeatureSettings):
    def __init__(self, *args, **kwargs):
        super(ConfigureHypervisor, self).__init__(*args, **kwargs)
        self.type = None
        self.server = None
        self.server_username = None
        self.server_password = None
        self.server_ssh_user = None
        self.server_ssh_passwd = None
        self.guest_ip = None
        self.guest_name = None
        self.guest_user = None
        self.guest_passwd = None

    def read(self, reader):
        self.type = get_exported_param("HYPERVISOR_TYPE")
        self.server = get_exported_param("HYPERVISOR_SERVER")
        self.server_username = get_exported_param("HYPERVISOR_USERNAME")
        self.server_password = get_exported_param("HYPERVISOR_PASSWORD")
        self.server_ssh_user = get_exported_param("HYPERVISOR_SSH_USER")
        self.server_ssh_passwd = get_exported_param("HYPERVISOR_SSH_PASSWD")
        self.guest_ip = get_exported_param("GUESR_IP")
        self.guest_name = get_exported_param("GUEST_NAME")
        self.guest_user = get_exported_param("GUEST_USER")
        self.guest_passwd = get_exported_param("GUEST_PASSWD")
        if not self.type:
            self.type = reader.get('hypervisor', 'type')
        if not self.server:
            self.server = reader.get('hypervisor', 'server')
        if not self.server_username:
            self.server_username = reader.get('hypervisor', 'server_username')
        if not self.server_password:
            self.server_password = reader.get('hypervisor', 'server_password')
        if not self.server_ssh_user:
            self.server_ssh_user = reader.get('hypervisor', 'server_ssh_user')
        if not self.server_ssh_passwd:
            self.server_ssh_passwd = reader.get('hypervisor', 'server_ssh_passwd')
        if not self.guest_ip:
            self.guest_ip = reader.get('hypervisor', 'guest_ip')
        if not self.guest_name:
            self.guest_name = reader.get('hypervisor', 'guest_name')
        if not self.guest_user:
            self.guest_user = reader.get('hypervisor', 'guest_user')
        if not self.guest_passwd:
            self.guest_passwd = reader.get('hypervisor', 'guest_passwd')

class ConfigureRegister(FeatureSettings):
    def __init__(self, *args, **kwargs):
        super(ConfigureRegister, self).__init__(*args, **kwargs)
        self.type = None
        self.server = None
        self.owner = None
        self.env = None
        self.admin_user = None
        self.admin_passwd = None
        self.ssh_user = None
        self.ssh_passwd = None

    def read(self, reader):
        self.type = get_exported_param("REGISTER_TYPE")
        self.server = get_exported_param("REGISTER_SERVER")
        self.owner = get_exported_param("REGISTER_OWNER")
        self.env = get_exported_param("REGISTER_ENV")
        self.admin_user = get_exported_param("REGISTER_ADMIN_USER")
        self.admin_passwd = get_exported_param("REGISTER_ADMIN_PASSWD")
        self.ssh_user = get_exported_param("REGISTER_SSH_USER")
        self.ssh_passwd = get_exported_param("REGISTER_SSH_PASSWD")
        if not self.type:
            self.type = reader.get('register', 'type')
        if not self.server:
            self.server = reader.get('register', 'server')
        if not self.owner:
            self.owner = reader.get('register', 'owner')
        if not self.env:
            self.env = reader.get('register', 'env')
        if not self.admin_user:
            self.admin_user = reader.get('register', 'admin_user')
        if not self.admin_passwd:
            self.admin_passwd = reader.get('register', 'admin_passwd')
        if not self.ssh_user:
            self.ssh_user = reader.get('register', 'ssh_user')
        if not self.ssh_passwd:
            self.ssh_passwd = reader.get('register', 'ssh_passwd')

class ConfigureManifest(FeatureSettings):
    def __init__(self, *args, **kwargs):
        super(ConfigureManifest, self).__init__(*args, **kwargs)
        self.vdc = None
        self.vdc_bonus = None
        self.instance = None
        self.limit = None
        self.unlimit = None

    def read(self, reader):
        self.vdc = reader.get('manifest', 'vdc')
        self.vdc_bonus = reader.get('manifest', 'vdc_bonus')
        self.instance = reader.get('manifest', 'instance')
        self.limit = reader.get('manifest', 'limit')
        self.unlimit = reader.get('manifest', 'unlimit')
        if not self.vdc:
            self.vdc = "RH00002"
        if not self.vdc_bonus:
            self.vdc_bonus = "RH00050"
        if not self.instance:
            self.instance = "RH00003"
        if not self.limit:
            self.limit = "RH00204"
        if not self.unlimit:
            self.unlimit = "RH00060"

class ConfigurePerformance(FeatureSettings):
    def __init__(self, *args, **kwargs):
        super(ConfigurePerformance, self).__init__(*args, **kwargs)
        self.vcenter_ip = None
        self.vcenter_admin_user = None
        self.vcenter_admin_passwd = None
        self.vcenter_ssh_user = None
        self.vcenter_ssh_passwd = None
        self.esxi_hosts = None
        self.esxi_hosts_user = None
        self.esxi_hosts_passwd = None

    def read(self, reader):
        self.vcenter_ip = reader.get('performance', 'vcenter_ip')
        self.vcenter_admin_user = reader.get('performance', 'vcenter_admin_user')
        self.vcenter_admin_passwd = reader.get('performance', 'vcenter_admin_passwd')
        self.vcenter_ssh_user = reader.get('performance', 'vcenter_ssh_user')
        self.vcenter_ssh_passwd = reader.get('performance', 'vcenter_ssh_passwd')
        self.esxi_hosts = reader.get('performance', 'esxi_hosts')
        self.esxi_hosts_user = reader.get('performance', 'esxi_hosts_user')
        self.esxi_hosts_passwd = reader.get('performance', 'esxi_hosts_passwd')

class ConfigSettings(Settings):
    def __init__(self):
        self.virtwho = ConfigureVirtwho()
        self.manifest = ConfigureManifest()
        self.hypervisor = ConfigureHypervisor()
        self.register = ConfigureRegister()
        self.performance = ConfigurePerformance()
