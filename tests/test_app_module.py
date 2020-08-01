from devinstaller import models as m


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
        obj = m.app_module.AppModule(**data)
        assert {"k1": "v1", "k2": "v2"} == obj.constants
        assert "cmd 1 v1" == obj.install_inst[0].cmd
        assert "rollback 1 v1" == obj.install_inst[0].rollback
        assert "cmd 2 v2" == obj.install_inst[1].cmd
        assert None == obj.install_inst[1].rollback

    def test_2(self):
        data = {"name": "test"}
        obj = m.app_module.AppModule(**data)
        assert {} == obj.constants
        assert None == obj.install_inst

    def test_3(self):
        data = {
            "name": "test",
            "constants": [{"key": "k1", "value": "v1"}, {"key": "k2", "value": "v2"}],
        }
        obj = m.app_module.AppModule(**data)
        assert {"k1": "v1", "k2": "v2"} == obj.constants
        assert None == obj.install_inst
