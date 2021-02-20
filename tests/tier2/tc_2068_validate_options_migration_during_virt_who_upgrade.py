# coding:utf-8
from virt_who import *
from virt_who.base import Base
from virt_who.register import Register
from virt_who.testing import Testing


class Testcase(Testing):
    def test_run(self):
        self.vw_case_info(os.path.basename(__file__), case_id='RHEL-198375')
        compose_id = self.get_config('rhel_compose')
        if compose_id not in ('RHEL-9', 'RHEL9'):
            self.vw_case_skip(compose_id)

        # Case Config
        results = dict()
        conf_file = "/etc/virt-who.conf"
        conf_file_backup = "/etc/virt-who.conf.backup"
        sysconfig_file = "/etc/sysconfig/virt-who"

        # Case Steps
        try:
            logger.info(">>>step1: configure and backup /etc/virt-who.conf")
            self.vw_etc_conf_disable_all()
            self.runcmd('cp {0} {1}'.format(conf_file, conf_file_backup), self.ssh_host())

            logger.info(">>>step2: create /etc/sysconfig/virt-who file")
            cmd = ('cat <<EOF > {0}\n'
                   'VIRTWHO_DEBUG = 1\n'
                   'VIRTWHO_ONE_SHOT = 0\n'
                   'VIRTWHO_INTERVAL = 120\n'
                   'http_proxy = squid.corp.redhat.com:3128\n'
                   'no_proxy = *\n'
                   'EOF'
                   ).format(sysconfig_file)
            self.runcmd(cmd, self.ssh_host())

            logger.info(">>>step3: run migrateconfiguration.py script")
            cmd = "/usr/bin/python3 /usr/lib/python3.9/site-packages/virtwho/migrate/migrateconfiguration.py"
            self.runcmd(cmd, self.ssh_host())

            logger.info(">>>step4: check the configurations in {0} are migrated to {1}"
                        .format(sysconfig_file, conf_file))
            ret, output = self.runcmd("cat {0}".format(conf_file), self.ssh_host())
            msg1 = "[global]\n" \
                   "#migrated\n" \
                   "interval=120\n" \
                   "#migrated\n" \
                   "debug=True\n" \
                   "#migrated\n" \
                   "oneshot=False"
            msg2 = "[system_environment]\n" \
                   "#migrated\n" \
                   "http_proxy=squid.corp.redhat.com:3128\n" \
                   "#migrated\n" \
                   "no_proxy=*"
            results.setdefault('step4', []).append(msg1 in output)
            results.setdefault('step4', []).append(msg2 in output)

        finally:
            logger.info(">>>step5: recover environments")
            self.runcmd('cp {0} {1} ; rm -f {0}'.format(conf_file_backup, conf_file),
                        self.ssh_host(), desc="recover the /etc/virt-who.conf file")
            self.runcmd('rm -f {0}'.format(sysconfig_file),
                        self.ssh_host(), desc="remove the /etc/sysconfig/virt-who file")

        # Case Result
        self.vw_case_result(results)
