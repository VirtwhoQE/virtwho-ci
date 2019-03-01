# coding:utf-8
from library import *
from library.base import Base
from library.virtwho import Virtwho

class Testcase(Virtwho):
    def test_run(self):
        # Case Header
        case_name = os.path.basename(__file__)
        self.vw_case_info(case_name, "RHEL-136711")
        mode, host_ip, guest_ip = self.vw_env_info()
        server_type, server_ip, owner, env = self.vw_server_info()
        if "libvirt-local" in mode or "vdsm" in mode:
            self.vw_case_skip("skipped - this case is not avaialbe for %s" % mode)
        self.vw_env_init(mode)

        # Case Config
        results = dict()
        conf_name = "%s_config" % mode.lower()
        conf_file = "/etc/virt-who.d/%s.conf" % mode.lower()
        invalid_file = "/etc/virt-who.d/%s.conf.txt" % mode.lower()
        self.vw_option_enable("VIRTWHO_DEBUG", filename="/etc/sysconfig/virt-who")
        self.vw_option_update_value("VIRTWHO_DEBUG", '1', filename="/etc/sysconfig/virt-who")
        self.vw_etc_d_mode_create(mode, conf_name, conf_file)

        # Case Steps
        logger.info(">>>step1: run virt-who with the expected config file name")
        data, tty_output, rhsm_output = self.vw_start()
        res = self.op_normal_value(data, exp_error=0, exp_thread=1, exp_send=1)
        results.setdefault('step1', []).append(res)

        logger.info(">>>step2: run virt-who with the unexpected config file name")
        logger.warning("libvirt-local mode will be used to instead when no valid config")
        cmd = "mv %s %s" % (conf_file, invalid_file)
        ret, output = self.runcmd(cmd, self.ssh_host(), desc="rename file")
        data, tty_output, rhsm_output = self.vw_start()
        res1 = self.op_normal_value(data, exp_error="1|2", exp_thread=1, exp_send=0)
        res2 = self.msg_validation(rhsm_output, ["Error in .* backend"], exp_exist=True)
        res3 = self.vw_msg_search(rhsm_output, "not have any .*conf.* files but is not empty", exp_exist=True)
        results.setdefault('step2', []).append(res1)
        results.setdefault('step2', []).append(res2)
        results.setdefault('step2', []).append(res3)

        # Case Result
        self.vw_case_result(results)
if __name__ == "__main__":
    unittest.main()

#===changelog===
#- 2018/07/30 Eko<hsun@redhat.com>
#- Case created
