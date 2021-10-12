from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible import errors


class FilterModule(object):
    ''' Get monitors ip addresses from a config file '''

    def get_monitors_ips(self, config):
        ip_list = []
        start_patterns = ['[v2:', 'v1:']
        for raw_line in config.split('\n'):
            if raw_line.replace('_', ' ').startswith('mon host ='):
                key, value = raw_line.split('=')
                value = value.strip()
                lines = value.split(',')
                for line in lines:
                    for start_pattern in start_patterns:
                        ip = ''
                        if line.startswith(start_pattern):
                            if line[len(start_pattern)] == '[':
                                # ipv6
                                for x in range(len(start_pattern), line.find(']')+1):
                                    ip += line[x]
                            else:
                                # ipv4
                                for x in range(len(start_pattern), line.rfind(':')):
                                    ip += line[x]
                        if ip:
                            ip_list.append(ip)

                return ','.join(list(set(ip_list)))

        raise errors.AnsibleFilterError("No line 'mon host' found in config.")

    def filters(self):
        return {'get_monitors_ips': self.get_monitors_ips}
