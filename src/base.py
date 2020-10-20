#-*- coding: utf-8 -*-
#!/usr/bin/python

from pyDiameter.pyDiaMessage import *
from pyDiameter.pyDiaAVPTools import *
from pyDiameter.pyDiaAVPPath import *
from pyDiameter.pyDiaAVPBasicTypes import *
from pyDiameter.pyDiaAVPDict import *
from pyDiameter.pyDiaAVPConst import *

def bit_mask(value, mask):
    result = int(bin(value & mask), 2)
    #print('result: %s %s %d' % (value, mask, result))

    if result == 0:
        return 0
    else:
        return 1

def display_cmd(cmd):
    print('Length: ', len(cmd))
    print('Flags: ', get_cmd_flags(cmd.getFlags()))
    print('Command Code: ', cmd.getCommandCode())
    print('ApplicationId: ', cmd.getApplicationID())
    print('Hop-By-Hop Identifier: ', cmd.getHBHID())
    print('End-to-End Identifier: ', cmd.getE2EID())

    avps = cmd.getAVPs()
    for avp in avps:
        display_avp(avp)

def get_cmd_flags(flags):
    str = ''
    if bit_mask(flags, 0x80) == 1:
        str += 'Request '
    else:
        str += 'Answer '
    if bit_mask(flags, 0x40) == 1:
        str += 'Proxyable '
    if bit_mask(flags, 0x20) == 1:
        str += 'Error '
    if bit_mask(flags, 0x10) == 1:
        str += 'T '
    return str

def display_avp(avp, tab=''):                   
    print(tab,end='')                        
    print('AVP Name:  ', avp.getAVPName())        
    print(tab,end='')                        
    print('AVP Type:  ', avp.getAVPType())        
    print(tab,end='')                        
    print('AVP Code:  ', avp.getAVPCode())        
    print(tab,end='')                        
    print('AVP Flags: ', get_avp_flags(avp.getAVPFlags()))       
    print(tab,end='')                        
    print('AVP Length:   ', len(avp))                
    value=avp.getAVPValue()                  
    if avp.getAVPVSFlag():                   
        print(tab,end='')                    
        print('AVP Vendor ID:', avp.getAVPVendor()) 
    if type(value) is list:                  
        print(tab, end='')                   
        print('===>')                       
        for sub in value:                    
            display_avp(sub, tab+'    ')        
        print(tab, end='')                   
        print('<===')                       
    else:                                    
        print(tab,end='')                    
        print('AVP Value: ', value)              
    print(tab,end='')                        
    print('-------')                         

def get_avp_flags(flags):
    str = ''
    if bit_mask(flags, 0x80) == 1:
        str += 'Vendor-Specific '
    if bit_mask(flags, 0x40) == 1:
        str += 'Mandatory '
    if bit_mask(flags, 0x20) == 1:
        str += 'Protected '
    return str

def make_hdr(argv): # flags, code, appId, hbhId, e2dId
    cmd = DiaMessage()
    cmd.setFlags(argv[0])
    cmd.setCommandCode(argv[1])
    cmd.setApplicationID(argv[2])
    cmd.setHBHID(argv[3])
    cmd.setE2EID(argv[4])

    return cmd

def make_avp(argv): #code, flags, vendor, value
    code, flags, vendor, value = argv

    dict = DiaAVPDict()
    if dict.getAVPDefType(vendor, code) == AVP_TYPE_STR:
        avp = DiaAVPStr()
    elif dict.getAVPDefType(vendor, code) == AVP_TYPE_INT32:
        avp = DiaAVPInt32()
    elif dict.getAVPDefType(vendor, code) == AVP_TYPE_UINT32:
        avp = DiaAVPUInt32()
    elif dict.getAVPDefType(vendor, code) == AVP_TYPE_INT64:
        avp = DiaAVPInt64()
    elif dict.getAVPDefType(vendor, code) == AVP_TYPE_UINT64:
        avp = DiaAVPUInt64()
    elif dict.getAVPDefType(vendor, code) == AVP_TYPE_FLOAT32:
        avp = DiaAVPFloat32()
    elif dict.getAVPDefType(vendor, code) == AVP_TYPE_FLOAT64:
        avp = DiaAVPFloat64()
    else:
        return ''

    avp.setAVPCode(code)
    if bit_mask(flags, 0x80) == 1:
        avp.setAVPVSFlag()
        avp.setAVPVendor(vendor)
    if bit_mask(flags, 0x40) == 1:
        avp.setAVPMandatoryFlag()
    if bit_mask(flags, 0x20) == 1:
        avp.setAVPProtectdAVP()

    if code == 257 or code == 501: # Host-IP-Address
        avp.setAVPValue(address_to_bytes(('ipv4', value)))
    else:
        if value != None:
            avp.setAVPValue(value)

    return avp

def make_avp_group(argv):
    code, flags, vendor, value = argv

    avp = DiaAVPGroup()
    avp.setAVPCode(code)
    if bit_mask(flags, 0x80) == 1:
        avp.setAVPVSFlag()
        avp.setAVPVendor(vendor)
    if bit_mask(flags, 0x40) == 1:
        avp.setAVPMandatoryFlag()
    if bit_mask(flags, 0x20) == 1:
        avp.setAVPProtectdAVP()
    return avp

def append_avp(cmd, avp):
    avpPath = DiaAVPPath()
    avpPath.setPath('')
    cmd.addAVPByPath(avpPath, avp)

def append_sub_avp(cmd, avp, path):
    avpPath = DiaAVPPath()
    avpPath.setPath(path)
    cmd.addAVPByPath(avpPath, avp)