# coding:utf-8
from library import *
from library.base import Base
from library.virtwho import Virtwho

class Testcase(Virtwho):
    def test_run(self):
        # Case Header
        case_name = os.path.basename(__file__)
        self.vw_case_info(case_name, "RHEL-136637")
        mode, host_ip, guest_ip = self.vw_env_info()
        server_type, server_ip, owner, env = self.vw_server_info()
        if "libvirt-local" in mode or "vdsm" in mode:
            self.vw_case_skip("skipped - this case is not avaialbe for %s" % mode)
        self.vw_env_init(mode)

        # Case Config
        results = dict()
        conf_name = "%s_config" % mode
        conf_file = "/etc/virt-who.d/%s.conf" % mode
        host_uuid = self.mode_host_uuid(mode)
        self.vw_option_enable("VIRTWHO_DEBUG", filename="/etc/sysconfig/virt-who")
        self.vw_option_update_value("VIRTWHO_DEBUG", '1', filename="/etc/sysconfig/virt-who")
        self.vw_etc_d_mode_create(mode, conf_name, filename=conf_file)

        # Case Steps
        logger.info(">>>step1: run virt-who with filter_hosts=''")
        self.vw_option_add("filter_hosts", r"''", conf_file)
        data, tty_output, rhsm_output = self.vw_start()
        s1 = self.op_normal_value(data, exp_error=0, exp_thread=1, exp_send=1)
        results.setdefault('step1', []).append(s1)
        s2 = self.vw_msg_search(str(data), host_uuid, exp_exist=False)
        results.setdefault('step1', []).append(s2)

        logger.info('>>>step2: run virt-who with filter_hosts=""')
        self.vw_option_update_value("filter_hosts", r'\"\"', conf_file)
        data, tty_output, rhsm_output = self.vw_start()
        s1 = self.op_normal_value(data, exp_error=0, exp_thread=1, exp_send=1)
        results.setdefault('step2', []).append(s1)
        s2 = self.vw_msg_search(str(data), host_uuid, exp_exist=False)
        results.setdefault('step2', []).append(s2)

        logger.info(">>>step3: run virt-who with filter_hosts='host_uuid'")
        self.vw_option_update_value("filter_hosts", r"'%s'" % host_uuid, conf_file)
        data, tty_output, rhsm_output = self.vw_start()
        s1 = self.op_normal_value(data, exp_error=0, exp_thread=1, exp_send=1)
        results.setdefault('step1', []).append(s1)
        s2 = self.vw_msg_search(str(data), host_uuid, exp_exist=True)
        results.setdefault('step1', []).append(s2)

        logger.info('>>>step4: run virt-who with filter_hosts="host_uuid"')
        self.vw_option_update_value("filter_hosts", r'\"%s\"' % host_uuid, conf_file)
        data, tty_output, rhsm_output = self.vw_start()
        s1 = self.op_normal_value(data, exp_error=0, exp_thread=1, exp_send=1)
        results.setdefault('step4', []).append(s1)
        s2 = self.vw_msg_search(str(data), host_uuid, exp_exist=True)
        results.setdefault('step4', []).append(s2)
        self.vw_option_del("filter_hosts", conf_file)

        logger.info(">>>step5: run virt-who with exclude_hosts=''")
        self.vw_option_add("exclude_hosts", r"''", conf_file)
        data, tty_output, rhsm_output = self.vw_start()
        s1 = self.op_normal_value(data, exp_error=0, exp_thread=1, exp_send=1)
        results.setdefault('step5', []).append(s1)
        s2 = self.vw_msg_search(str(data), host_uuid, exp_exist=True)
        results.setdefault('step5', []).append(s2)

        logger.info('>>>step6: run virt-who with exclude_hosts=""')
        self.vw_option_update_value("exclude_hosts", r'\"\"', conf_file)
        data, tty_output, rhsm_output = self.vw_start()
        s1 = self.op_normal_value(data, exp_error=0, exp_thread=1, exp_send=1)
        results.setdefault('step6', []).append(s1)
        s2 = self.vw_msg_search(str(data), host_uuid, exp_exist=True)
        results.setdefault('step6', []).append(s2)

        logger.info(">>>step7: run virt-who with exclude_hosts='host_uuid'")
        self.vw_option_update_value("exclude_hosts", r"'%s'" % host_uuid, conf_file)
        data, tty_output, rhsm_output = self.vw_start()
        s1 = self.op_normal_value(data, exp_error=0, exp_thread=1, exp_send=1)
        results.setdefault('step7', []).append(s1)
        s2 = self.vw_msg_search(str(data), host_uuid, exp_exist=False)
        results.setdefault('step7', []).append(s2)

        logger.info('>>>step8: run virt-who with exclude_hosts="host_uuid"')
        self.vw_option_update_value("exclude_hosts", r'\"%s\"' % host_uuid, conf_file)
        data, tty_output, rhsm_output = self.vw_start()
        s1 = self.op_normal_value(data, exp_error=0, exp_thread=1, exp_send=1)
        results.setdefault('step8', []).append(s1)
        s2 = self.vw_msg_search(str(data), host_uuid, exp_exist=False)
        results.setdefault('step8', []).append(s2)
        self.vw_option_del("exclude_hosts", conf_file)

        # Case Result
        self.vw_case_result(results)
if __name__ == "__main__":
    unittest.main()

#===changelog===
#- 2018/07/16 Eko<hsun@redhat.com>
#- Case created to validate filter_hosts and exclude_hosts for quotes
