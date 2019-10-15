# coding:utf-8
from virt_who import *
from virt_who.base import Base
from virt_who.register import Register
from virt_who.testing import Testing


class Testcase(Testing):
    def test_run(self):
        self.vw_case_info(os.path.basename(__file__), case_id='RHEL-133748')
        compose_id = self.get_config('rhel_compose')
        if "RHEL-8" in compose_id:
            self.vw_case_skip("RHEL-8")
        self.vw_case_init()

        # case config
        results = dict()
        hypervisor_type = self.get_config('hypervisor_type')
        if 'kubevirt' in hypervisor_type:
            config_name = "virtwho-config"
            config_file = "/etc/virt-who.d/{0}.conf".format(config_name)
            self.vw_etc_d_mode_create(config_name, config_file)
            cmd1 = "virt-who --sam -d"
            cmd2 = "virt-who --satellite6 -d"
        else:
            cmd1 = self.vw_cli_base() + "--sam -d"
            cmd2 = self.vw_cli_base() + "--satellite6 -d"
        steps = {'step1': cmd1, 'step2': cmd2}

        # case steps
        for step, cmd in sorted(steps.items(), key=lambda item: item[0]):
            logger.info(">>>{0}: run virt-who cli to check sam/satellite options"
                        .format(step))
            data, tty_output, rhsm_output = self.vw_start(cmd, exp_send=1)
            s1 = self.op_normal_value(data, exp_error=0, exp_thread=1, exp_send=1)
            results.setdefault(step, []).append(s1)

        # case result
        notes = list()
        notes.append("Bug 1760175 - Remove --sam/--satellite6 or repair them?")
        self.vw_case_result(results, notes)
