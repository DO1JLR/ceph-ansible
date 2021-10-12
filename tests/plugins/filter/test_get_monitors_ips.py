from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import get_monitors_ips
import pytest
from ansible.errors import AnsibleFilterError


filter_plugin = get_monitors_ips.FilterModule()

CEPH_CONFIG_IPV4 = '''
[global]
auth_allow_insecure_global_id_reclaim = False
cluster network = 192.168.61.0/24
fsid = e8204e9a-a3f5-44a1-9097-ac508aac3f8d
mon host = [v2:10.0.0.1:3300/0,v1:10.0.0.1:6789/0],[v2:10.0.0.2:3300/0,v1:10.0.0.2:6789/0],[v2:10.0.0.3:3300/0,v1:10.0.0.3:6789/0]
mon initial members = mon0
''' # noqa : E501

CEPH_CONFIG_IPV6 = '''
[global]
auth_allow_insecure_global_id_reclaim = False
cluster network = fe80::/64
fsid = e8204e9a-a3f5-44a1-9097-ac508aac3f8d
mon host = [v2:[2a01:cb04:1d0:7300:6a3f:7dff:fecb:c870]:3300/0,v1:[2a01:cb04:1d0:7300:6a3f:7dff:fecb:c870]:6789/0],[v2:[2a01:cb04:1d0:7300:6a3f:7dff:fecb:c871]:3300/0,v1:[2a01:cb04:1d0:7300:6a3f:7dff:fecb:c871]:6789/0],[v2:[2a01:cb04:1d0:7300:6a3f:7dff:fecb:c872]:3300/0,v1:[2a01:cb04:1d0:7300:6a3f:7dff:fecb:c872]:6789/0]
mon initial members = mon0
''' # noqa : E501

CEPH_CONFIG_NO_MON_HOST = '''
[global]
auth_allow_insecure_global_id_reclaim = False
cluster network = fe80::/64
fsid = e8204e9a-a3f5-44a1-9097-ac508aac3f8d
mon initial members = mon0
'''


class TestGetMonitorsIps(object):
    def test_no_mon_host(self):
        with pytest.raises(AnsibleFilterError):
            filter_plugin.get_monitors_ips(CEPH_CONFIG_NO_MON_HOST)

    def test_ipv4(self):
        result = filter_plugin.get_monitors_ips(CEPH_CONFIG_IPV4)
        assert '10.0.0.1' in result
        assert '10.0.0.2' in result
        assert '10.0.0.3' in result

    def test_ipv6(self):
        result = filter_plugin.get_monitors_ips(CEPH_CONFIG_IPV6)
        assert "[2a01:cb04:1d0:7300:6a3f:7dff:fecb:c872]" in result
        assert "[2a01:cb04:1d0:7300:6a3f:7dff:fecb:c870]" in result
        assert "[2a01:cb04:1d0:7300:6a3f:7dff:fecb:c871]" in result
