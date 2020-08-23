from devinstaller_core import module_app as m


class TestConstants:
    def test_1(self):
        data = {
            "name": "test",
            "constants": [{"key": "k1", "value": "v1"}, {"key": "k2", "value": "v2"}],
            "install_inst": [
                {"cmd": "cmd 1 {k1}", "rollback": "rollback 1 {k1}"},
                {"cmd": "cmd 2 {k2}"},
            ],
        }
        obj = m.ModuleApp(**data)
        assert {"k1": "v1", "k2": "v2"} == obj.constants
        assert obj.install_inst[0].cmd == "cmd 1 v1"
        assert obj.install_inst[0].rollback == "rollback 1 v1"
        assert obj.install_inst[1].cmd == "cmd 2 v2"
        assert obj.install_inst[1].rollback is None

    def test_2(self):
        data = {"name": "test"}
        obj = m.ModuleApp(**data)
        assert obj.constants == {}
        assert obj.install_inst is None

    def test_3(self):
        data = {
            "name": "test",
            "constants": [{"key": "k1", "value": "v1"}, {"key": "k2", "value": "v2"}],
        }
        obj = m.ModuleApp(**data)
        assert obj.constants == {"k1": "v1", "k2": "v2"}
        assert obj.install_inst is None
