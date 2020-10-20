#-*- coding: utf-8 -*-
## !/usr/bin/python

import json

from base import *

class Command:
    def __init__(self, filepath):
        self.filepath = filepath

    def make_cmd(self):
        # Lodd json file
        with open(self.filepath) as file:
            dict = json.load(file)

        # Make a diameter command header
            cmd = make_hdr((int(dict['Flags'], 16), dict['Command Code'], dict['ApplicationId'], int(dict['Hop-by-Hop Identifier'], 16), int(dict['End-to-End Identifier'], 16)))

        # Make AVPs
            for avp in dict['AVPs']:
                if avp['Type'] == 'STR':
                    value = avp['Value'].encode('UTF-8')
                else:
                    value = avp['Value']

                code = avp['Code']
                flags = int(avp['Flags'], 16)
                vendor = avp['Vendor']

                if avp['Type'] == 'GROUP':
                    if avp['Path'] == "":
                        append_avp(cmd, make_avp_group((code, flags, vendor, None)))
                    else:
                        append_sub_avp(cmd, make_avp_group((code, flags, vendor, None)), avp['Path'])
                else:
                    if avp['Path'] == "":
                        append_avp(cmd, make_avp((code, flags, vendor, value)))
                    else:
                        append_sub_avp(cmd, make_avp((code, flags, vendor, value)), avp['Path'])

        display_cmd(cmd)

        # Close json file
        file.close()

        return cmd.encode()

# Example 
cmd = Command('../data/dwr.json')
cmd.make_cmd()
