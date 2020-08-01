from devinstaller import models as m


class TestInterfaceBlock:
    def test_1(self):
        int_list = [{"name": "interface 1"}, {"name": "interface 2"}]
        interface_name = "interface 1"
        interface = m.get_interface(
            interface_list=int_list, interface_name=interface_name
        )
        assert isinstance(interface, m.InterfaceBlock)
