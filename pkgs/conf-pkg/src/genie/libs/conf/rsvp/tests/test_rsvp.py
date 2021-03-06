#!/usr/bin/env python

import unittest
from unittest.mock import Mock
from genie.conf.tests import TestCase

import re

from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

from genie.libs.conf.rsvp import Rsvp


class test_rsvp(TestCase):

    def setUp(self):
        tb = Genie.testbed = Testbed()
        self.dev1 = Device(testbed = tb, name='PE1', os='iosxr')
        self.dev2 = Device(testbed = tb, name='PE2', os='iosxr')
        self.i1 = Interface(name='GigabitEthernet0/0/0/1', device=self.dev1)
        self.i2 = Interface(name='GigabitEthernet0/0/0/2', device=self.dev2)
        self.i3 = Interface(name='GigabitEthernet0/0/0/3', device=self.dev1)
        self.i4 = Interface(name='GigabitEthernet0/0/0/4', device=self.dev2)
        self.i5 = Interface(name='GigabitEthernet0/0/0/5', device=self.dev1)
        self.i6 = Interface(name='GigabitEthernet0/0/0/6', device=self.dev2)
        self.i7 = Interface(name='GigabitEthernet0/0/0/7', device=self.dev1)
        self.i8 = Interface(name='GigabitEthernet0/0/0/8', device=self.dev2)
        self.link = Link(name='1_2_1')
        self.link.connect_interface(interface=self.i1)
        self.link.connect_interface(interface=self.i2)
        self.link2 = Link(name='1_2_2')
        self.link2.connect_interface(interface=self.i3)
        self.link2.connect_interface(interface=self.i4)
        self.link3 = Link(name='1_2_3')
        self.link3.connect_interface(interface=self.i5)
        self.link3.connect_interface(interface=self.i6)
        self.link4 = Link(name='1_2_4')
        self.link4.connect_interface(interface=self.i7)
        self.link4.connect_interface(interface=self.i8)
        self.assertCountEqual(
            self.link.find_interfaces(),
            [self.i1, self.i2])
        self.assertCountEqual(
            self.dev1.find_interfaces(),
            [self.i1, self.i3, self.i5, self.i7])
        self.assertCountEqual(
            self.dev2.find_interfaces(),
            [self.i2, self.i4, self.i6, self.i8])

    def test_0_interface_only(self):

        rsvp = Rsvp()
        self.assertCountEqual(rsvp.devices, [])
        self.assertCountEqual(rsvp.links, [])
        self.assertCountEqual(rsvp.interfaces, [])

        self.link.add_feature(rsvp)
        self.link2.add_feature(rsvp)
        self.link3.add_feature(rsvp)
        self.link4.add_feature(rsvp)
        self.assertCountEqual(rsvp.devices, [self.dev1, self.dev2])
        self.assertCountEqual(rsvp.links, [self.link, self.link2, self.link3, self.link4])
        self.assertCountEqual(rsvp.interfaces, [self.i1, self.i2, self.i3, self.i4, self.i5, self.i6, self.i7, self.i8])

        rsvp.device_attr[self.i1.device].interface_attr[self.i1].rdm_bw_total = None
        rsvp.device_attr[self.i1.device].interface_attr[self.i3].rdm_bw_cli_rdm_kw = False
        rsvp.device_attr[self.i1.device].interface_attr[self.i5].rdm_bw_cli_style = Rsvp.RdmBwCliStyle.bc0_bc1
        rsvp.device_attr[self.i1.device].interface_attr[self.i7].rdm_bw_cli_style = Rsvp.RdmBwCliStyle.global_subpool
        cfgs = rsvp.build_config(apply=False)
        self.assertMultiLineDictEqual(cfgs, {
            self.dev1.name: '\n'.join([
                'rsvp',
                ' interface GigabitEthernet0/0/0/1',
                '  exit',
                ' interface GigabitEthernet0/0/0/3',
                '  bandwidth 20000 20000',
                '  exit',
                ' interface GigabitEthernet0/0/0/5',
                '  bandwidth rdm bc0 20000 20000',
                '  exit',
                ' interface GigabitEthernet0/0/0/7',
                '  bandwidth rdm global-pool 20000 20000',
                '  exit',
                ' exit',
            ]),
            self.dev2.name: '\n'.join([
                'rsvp',
                ' interface GigabitEthernet0/0/0/2',
                '  bandwidth rdm 20000 20000',
                '  exit',
                ' interface GigabitEthernet0/0/0/4',
                '  bandwidth rdm 20000 20000',
                '  exit',
                ' interface GigabitEthernet0/0/0/6',
                '  bandwidth rdm 20000 20000',
                '  exit',
                ' interface GigabitEthernet0/0/0/8',
                '  bandwidth rdm 20000 20000',
                '  exit',
                ' exit',
            ]),
        })

if __name__ == '__main__':
    unittest.main()

