#!/usr/bin/env python3
"""Offline ARMv7-M fault register interpretation; no target/probe operations."""
import argparse
import json
from pathlib import Path

CFSR={0:'IACCVIOL',1:'DACCVIOL',3:'MUNSTKERR',4:'MSTKERR',5:'MLSPERR',7:'MMARVALID',
      8:'IBUSERR',9:'PRECISERR',10:'IMPRECISERR',11:'UNSTKERR',12:'STKERR',13:'LSPERR',15:'BFARVALID',
      16:'UNDEFINSTR',17:'INVSTATE',18:'INVPC',19:'NOCP',24:'UNALIGNED',25:'DIVBYZERO'}
HFSR={1:'VECTTBL',30:'FORCED',31:'DEBUGEVT'}

def register(value):
    if isinstance(value,str):
        try:value=int(value,0)
        except ValueError:raise ValueError('invalid-register') from None
    if type(value) is not int or not 0<=value<=0xffffffff:
        raise ValueError('register-must-be-unsigned-32-bit')
    return value

def decode(capture):
    if not isinstance(capture,dict) or capture.get('architecture') not in ('cortex-m3','cortex-m4','cortex-m7'):
        raise ValueError('unsupported-architecture')
    if not {'cfsr','hfsr'}<=capture.keys():raise ValueError('missing-fault-registers')
    regs={k:register(capture[k]) for k in ('cfsr','hfsr','bfar','mmfar','pc','lr','sp','xpsr') if k in capture}
    c,h=regs['cfsr'],regs['hfsr']
    cfsr_fields={bit:name for bit,name in CFSR.items() if capture['architecture']!='cortex-m3' or bit not in (5,13)}
    limitations=['capture-does-not-establish-device-health','matching-elf-and-build-required','root-cause-needs-corroboration']
    valid={}
    for key,bit in (('mmfar',7),('bfar',15)):
        if c&(1<<bit):
            if key in regs:valid[key]=f'0x{regs[key]:08x}'
            else:limitations.append(key+'-valid-but-not-captured')
    if c&(1<<10):limitations.append('stacked-pc-may-not-identify-origin')
    if c&sum(1<<b for b in (3,4,5,11,12,13) if b in cfsr_fields):
        limitations.append('stack-frame-may-be-unreliable')
    return {'schema_version':1,'evidence':'offline-register-interpretation','architecture':capture['architecture'],
            'registers':{k:f'0x{v:08x}' for k,v in regs.items()},
            'cfsr_flags':[name for bit,name in cfsr_fields.items() if c&(1<<bit)],
            'hfsr_flags':[name for bit,name in HFSR.items() if h&(1<<bit)],
            'unmapped_cfsr_bits':f'0x{c & ~sum(1<<b for b in cfsr_fields):08x}',
            'unmapped_hfsr_bits':f'0x{h & ~sum(1<<b for b in HFSR):08x}',
            'valid_fault_addresses':valid,'root_cause':None,'limitations':limitations}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('capture',type=Path);args=p.parse_args()
    try:
        if args.capture.stat().st_size>65536:raise ValueError('capture-too-large')
        result=decode(json.loads(args.capture.read_text(encoding='utf-8')))
    except (OSError,ValueError,TypeError):
        print(json.dumps({'status':'unresolved','reason':'invalid-unreadable-oversized-or-unsupported-capture'}));return 2
    print(json.dumps(result,indent=2));return 0

if __name__=='__main__':raise SystemExit(main())
