# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from ats.topology import Device

# Genie
from genie.libs.ops.interface.iosxe.c3850.interface import Interface
from genie.libs.ops.interface.iosxe.c3850.tests.interface_output import InterfaceOutput

# iosxe show_interface
from genie.libs.parser.iosxe.show_interface import ShowInterfaces, \
                                        ShowInterfacesSwitchport, \
                                        ShowIpInterface,  \
                                        ShowIpv6Interface, \
                                        ShowInterfacesAccounting
                                        
from genie.libs.parser.iosxe.show_vrf import ShowVrfDetail


class test_interface(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxe'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device

    def test_complete_output(self):
        self.maxDiff = None
        intf = Interface(device=self.device)
        # Get outputs
        intf.maker.outputs[ShowInterfaces] = \
            {'':InterfaceOutput.ShowInterfaces}

        intf.maker.outputs[ShowInterfacesSwitchport] = \
            {'':InterfaceOutput.ShowInterfacesSwitchport}

        intf.maker.outputs[ShowIpInterface] = \
            {'':InterfaceOutput.ShowIpInterface}

        intf.maker.outputs[ShowIpv6Interface] = \
            {'':InterfaceOutput.ShowIpv6Interface}

        intf.maker.outputs[ShowVrfDetail] = \
            {'':InterfaceOutput.ShowVrfDetail}

        intf.maker.outputs[ShowInterfacesAccounting] = \
            {'':InterfaceOutput.ShowInterfacesAccounting}

        # Learn the feature
        intf.learn()

        # Verify Ops was created successfully
        self.assertEqual(intf.info, InterfaceOutput.InterfaceOpsOutput_info)

    def test_empty_output(self):
        self.maxDiff = None
        intf = Interface(device=self.device)
        # Get outputs
        intf.maker.outputs[ShowInterfaces] = {'':''}
        intf.maker.outputs[ShowInterfacesSwitchport] = {'':''}
        intf.maker.outputs[ShowIpInterface] = {'':''}
        intf.maker.outputs[ShowIpv6Interface] = {'':''}
        intf.maker.outputs[ShowVrfDetail] = {'':''}
        intf.maker.outputs[ShowInterfacesAccounting] = {'':''}

        # Learn the feature
        intf.learn()

        # Check no attribute not found
        # info - oper_status
        with self.assertRaises(AttributeError):
            vrf = (intf.info['GigabitEthernet1/0/2']['oper_status'])

    def test_selective_attribute(self):
        self.maxDiff = None
        intf = Interface(device=self.device)
        # Get outputs
        intf.maker.outputs[ShowInterfaces] = \
            {'':InterfaceOutput.ShowInterfaces}

        intf.maker.outputs[ShowInterfacesSwitchport] = \
            {'':InterfaceOutput.ShowInterfacesSwitchport}

        intf.maker.outputs[ShowIpInterface] = \
            {'':InterfaceOutput.ShowIpInterface}

        intf.maker.outputs[ShowIpv6Interface] = \
            {'':InterfaceOutput.ShowIpv6Interface}

        intf.maker.outputs[ShowVrfDetail] = \
            {'':InterfaceOutput.ShowVrfDetail}

        intf.maker.outputs[ShowInterfacesAccounting] = \
            {'':InterfaceOutput.ShowInterfacesAccounting}

        # Learn the feature
        intf.learn()        

        # Check specific attribute values
        # info - vrf
        self.assertEqual(intf.info['GigabitEthernet0/0']['vrf'], 'Mgmt-vrf')
        # info - link_status
        self.assertEqual(intf.info['GigabitEthernet1/0/2']['oper_status'], 'up')

    def test_incomplete_output(self):
        self.maxDiff = None
        intf = Interface(device=self.device)
        # Get outputs
        intf.maker.outputs[ShowInterfaces] = \
            {'':InterfaceOutput.ShowInterfaces}

        intf.maker.outputs[ShowInterfacesSwitchport] = \
            {'':InterfaceOutput.ShowInterfacesSwitchport}

        intf.maker.outputs[ShowIpInterface] = {'':''}

        intf.maker.outputs[ShowIpv6Interface] = \
            {'':InterfaceOutput.ShowIpv6Interface}

        intf.maker.outputs[ShowVrfDetail] = \
            {'':InterfaceOutput.ShowVrfDetail}

        intf.maker.outputs[ShowInterfacesAccounting] = \
            {'':InterfaceOutput.ShowInterfacesAccounting}

        # Learn the feature
        intf.learn()        

        # Delete missing specific attribute values
        expect_dict = deepcopy(InterfaceOutput.InterfaceOpsOutput_info)
        del(expect_dict['GigabitEthernet1/0/1']['ipv4'])
        del(expect_dict['GigabitEthernet0/0']['ipv4'])
        del(expect_dict['Vlan100']['ipv4'])
                
        # Verify Ops was created successfully
        self.assertEqual(intf.info, expect_dict)


if __name__ == '__main__':
    unittest.main()
