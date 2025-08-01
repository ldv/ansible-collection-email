# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.utils.display import Display

display = Display()


class FilterModule(object):
    """
    """

    def filters(self):
        return {
            'postfix_map_data': self.postfix_map_data,
            'valid_list_data': self.valid_list_data,
            'sasl_data': self.sasl_data,
            'relay_data': self.relay_data,
        }

    def postfix_map_data(self, data):
        """
        """
        # display.v(f"postfix_map_data({data})")

        key = None
        values = None

        if isinstance(data, dict):
            key = data[list(data.keys())[0]]
            values = data[list(data.keys())[1]]

            if isinstance(values, list):
                values = ", ".join(values)
        # display.v(f"= result: {key} {values}")
        return key, values

    def valid_list_data(self, data, valid_entries):
        """
        """
        result = []

        if isinstance(data, list):
            data.sort()
            valid_entries.sort()
            result = list(set(data).intersection(valid_entries))
            result.sort()
        # display.v(f"=result: {result}")
        return result

    def sasl_data(self, data, mxlookup=False):
        """
            enhance sasl data for valid relay host and port
        """
        if isinstance(data, dict):
            username = data.get("username", None)
            host = data.get("host", None)
            port = data.get("port", None)

            if not host or not port:
                data["host"] = username
            else:
                if port:
                    _ = data.pop("port")

                # https://www.postfix.org/postconf.5.html#relayhost
                # The form [hostname] turns off MX lookups
                if not mxlookup:
                    data["host"] = f"[{host}]:{port}"
                else:
                    data["host"] = f"{host}:{port}"

        return data

    def relay_data(self, data, sasl_data, mxlookup=False):
        """
            enhance relay data for valid relay host and port
        """
        result = None

        if isinstance(data, dict):
            username = data.get("username", None)
            host = data.get("host", None)
            port = data.get("port", None)

            sasl = {k: v for data in sasl_data for k, v in data.items() if data.get("username") == username}

            if len(sasl) == 0:

                data["error"] = True
                data["msg"] = f"The user name '{username}' is not present in the SASL configuration."

                result = data

            else:
                data["error"] = False
                data["msg"] = None

                if not host or not port:
                    data["host"] = username
                else:
                    if port:
                        _ = data.pop("port")

                    # https://www.postfix.org/postconf.5.html#relayhost
                    # The form [hostname] turns off MX lookups
                    if not mxlookup:
                        data["host"] = f"[{host}]:{port}"
                    else:
                        data["host"] = f"{host}:{port}"

                result = data

        # display.v(f"=result: {result}")
        return result
