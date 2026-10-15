#!/usr/bin/env python3
"""Run reviewed compile-only fixtures. SDK checkout and tool installation are separate."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
PINS={'pico-sdk':'a1438dff1d38bd9c65dbd693f0e5db4b9ae91779',
      'micropython':'647c8b96cae7e202c7a020395b7cfe65e5b8ce04'}

def native_plan(kind,source,output,toolchain=None,host=None):
    source=Path(source).resolve();output=Path(output).resolve();host=host or platform.system()
    if output==source or output.is_relative_to(source) or source.is_relative_to(output):
        raise ValueError('SDK source and build directory must be separate')
    if kind=='pico-sdk':
        if not toolchain:raise ValueError('Pico SDK requires a selected Arm GCC toolchain directory')
        return [['cmake','-S',str(ROOT/'tests/fixtures/platforms/pico-sdk'),'-B',str(output),'-G','Ninja',
                 '-DPICO_BOARD=pico','-DPICO_PLATFORM=rp2040','-DCMAKE_BUILD_TYPE=Debug',
                 '-DPICO_SDK_PATH='+str(source),'-DPICO_TOOLCHAIN_PATH='+str(Path(toolchain).resolve())],
                ['cmake','--build',str(output),'--parallel','4']]
    if kind!='micropython':raise ValueError('unsupported native fixture')
    if host=='Windows':raise ValueError('Unix MicroPython fixture requires POSIX or WSL; native Windows not claimed')
    cmd=['make','-C',str(source/'ports/unix'),'VARIANT=minimal','BUILD='+str(output),'-j','4']
    if host=='Darwin':
        # v1.26.1 Darwin realtime code needs pthread declarations even in minimal.
        # Retain warnings; only the observed Clang constant-folding warning is nonfatal.
        cmd+=['MICROPY_PY_THREAD=1','CFLAGS_EXTRA=-Wno-error=gnu-folding-constant']
    return [cmd,[str(output/'micropython'),str(ROOT/'tests/fixtures/platforms/micropython/smoke.py')]]

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--platform',required=True,choices=['stm32cube','zephyr','pico-sdk','micropython'])
    p.add_argument('--source',type=Path);p.add_argument('--toolchain',type=Path)
    p.add_argument('--build-dir',type=Path,required=True)
    a=p.parse_args();output=a.build_dir.resolve();source_revision=None
    try:
        if a.build_dir.is_symlink() or (output.exists() and any(output.iterdir())):
            raise ValueError('use a fresh empty build directory; no automatic cleanup')
        if a.platform in PINS:
            if not a.source:raise ValueError('a pinned local SDK source checkout is required')
            source=a.source.resolve()
            source_revision=subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip()
            if source_revision!=PINS[a.platform]:raise ValueError('SDK source revision differs from fixture pin')
            dirty=subprocess.check_output(['git','-c','core.fsmonitor=false','-C',str(source),'status','--porcelain','--untracked-files=no'],text=True)
            if dirty:raise ValueError('tracked SDK source changes must be reviewed separately')
            commands=native_plan(a.platform,source,output,a.toolchain)
        else:
            commands=[[sys.executable,'-m','platformio','run','--project-dir',str(ROOT/'tests/fixtures/platforms'/a.platform),
                       '--environment','stm32cube-f401' if a.platform=='stm32cube' else 'zephyr-f401']]
        output.mkdir(parents=True,exist_ok=True)
        # PIO's build artifacts live under its reviewed fixture; build-dir stores logs/evidence.
        results=[]
        for i,cmd in enumerate(commands):
            log=output/f'step-{i}.log'
            with log.open('w') as handle:
                completed=subprocess.run(cmd,cwd=ROOT,stdout=handle,stderr=subprocess.STDOUT,check=False)
            results.append({'argv':cmd,'exit_code':completed.returncode,'log':str(log),
                            'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()})
            if completed.returncode:break
        record={'platform':a.platform,'host':platform.platform(),'python':sys.version.split()[0],
                'source_revision':source_revision,'evidence':'compile-only or Unix host smoke; no hardware access',
                'results':results,'passed':all(x['exit_code']==0 for x in results)}
        (output/'result.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
        return 0 if record['passed'] else 1
    except (OSError,ValueError,subprocess.CalledProcessError) as error:
        p.error(str(error))

if __name__=='__main__':raise SystemExit(main())
