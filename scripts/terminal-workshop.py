#!/usr/bin/env python3
"""Fresh 05Shaibaan terminal views; native screenshot portal, never imitation images."""
from pathlib import Path
import datetime
import hashlib
import importlib.util
import json
import shlex
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
SHARED=Path('/home/mirza/jenkins-assignment')
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('native_capture_tool',SHARED/'scripts/terminal-evidence.py')
portal=importlib.util.module_from_spec(spec);spec.loader.exec_module(portal)
STAMP=datetime.datetime.now().astimezone().strftime('%Y%m%dT%H%M%S')
NAMES=['runtime','welcome','fresh-maven','jar-execution','scm-detection','failure','recovery','release','release-gate']
report={'account':'05Shaibaan','started':datetime.datetime.now().astimezone().isoformat(),'screenshots':[]}

def command(args):
    print('$ '+shlex.join(args),flush=True)
    subprocess.run(args,cwd=ROOT,check=True)

def recorded(filename,job,build,pattern=None):
    print(f'{job} #{build} | saved output from earlier run | this 05Shaibaan lab only',flush=True)
    args=['grep','-E',pattern,filename] if pattern else ['cat',filename]
    command(args)

def header(title):
    print('\033[2J\033[H',end='')
    print('\033[1;36m'+'='*110)
    print('05SHAIBAAN / SIGNED ARITHMETIC DELIVERY WORKSHOP / '+title)
    print('='*110+'\033[0m')
    print('Terminal session: '+datetime.datetime.now().astimezone().isoformat(timespec='seconds'),flush=True)

def capture(name):
    rawdir=ROOT/'.lab/raw-terminal';rawdir.mkdir(exist_ok=True)
    raw=rawdir/name
    portal.capture(raw)
    with Image.open(raw) as full:
        full=full.convert('RGB')
        if full.size!=(5431,1615):raise RuntimeError('Desktop layout changed; select the terminal manually before publishing.')
        candidates=[(0,0,2560,1440),(2560,0,5431,1615)]
        scores=[]
        for box in candidates:
            band=full.crop((box[0],0,box[2],220))
            scores.append(sum(1 for r,g,b in band.getdata() if r<140 and g>150 and b>150))
        order=sorted(range(2),key=lambda i:scores[i],reverse=True)
        if scores[order[0]]<500 or scores[order[0]]<2*scores[order[1]]:
            raise RuntimeError('Cannot confidently isolate the cyan workshop terminal; raw capture kept private.')
        box=candidates[order[0]]
        cropped=full.crop(box)
        out=ROOT/'evidence/screenshots'/name
        if out.exists():raise RuntimeError('Refusing to replace an existing image')
        cropped.save(out)
        assert cropped.tobytes()==full.crop(box).tobytes()
    report['screenshots'].append({'path':'evidence/screenshots/'+name,
        'nativeCapture':'Ubuntu screenshot portal / real GNOME Terminal','crop':list(box),
        'operation':'lossless crop only; no rendered or substituted text',
        'rawPublished':False,'rawSha256':hashlib.sha256(raw.read_bytes()).hexdigest(),
        'sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
    (ROOT/'evidence/terminal-session.json').write_text(json.dumps(report,indent=2)+'\n')

for index,name in enumerate(NAMES,1):
    header(f'{index:02d} / {name.upper()}')
    if index==1:
        print('LIVE checks. Jenkins, Maven and the cache are reused; every job/result is new.')
        command(['lsb_release','-ds']);command(['java','-version']);command(['javac','-version']);command(['git','--version'])
        command([str(SHARED/'.lab/tools/apache-maven-3.9.16/bin/mvn'),'--version'])
        command(['systemctl','--user','status','jenkins-assignment','--no-pager','-n','0'])
        command(['bash','-c','curl -fsSI http://127.0.0.1:8080/ | grep -i "^X-Jenkins:"'])
        command(['git','log','-1','--format=Owner-local author: %an <%ae>'])
    elif index==2:
        recorded('evidence/logs/shaibaan05-welcome-1.txt','shaibaan05-welcome',1)
    elif index==3:
        args=[str(SHARED/'.lab/tools/apache-maven-3.9.16/bin/mvn'),'-o','-B','-ntp',
              '-Dmaven.repo.local='+str(SHARED/'.lab/m2'),'clean','package']
        print('FRESH command executing now: '+shlex.join(args),flush=True)
        result=subprocess.run(args,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        result.check_returncode()
        transcript=ROOT/'evidence'/f'local-build-{STAMP}.txt';transcript.write_text(result.stdout)
        suite=ET.parse(ROOT/'target/surefire-reports/TEST-dev.shaibaan.calculator.SignedCalculatorTest.xml').getroot()
        assert [suite.get(k) for k in ['tests','failures','errors','skipped']]==['2','0','0','0']
        print('Fresh execution completed in this terminal; final 29 lines of unmodified stdout:')
        print('\n'.join(result.stdout.splitlines()[-29:]),flush=True)
        report['freshMaven']={'transcript':str(transcript.relative_to(ROOT)),'tests':2,'failures':0,'offline':True,'newExecution':True}
    elif index==4:
        print('LIVE verification of the freshly generated 05Shaibaan JAR.')
        command(['ls','-lh','target/shaibaan-calculator-1.1.0.jar'])
        command(['sha256sum','target/shaibaan-calculator-1.1.0.jar'])
        command(['java','-jar','target/shaibaan-calculator-1.1.0.jar'])
    elif index==5:
        recorded('evidence/scm-detection-build-2.txt','shaibaan05-calculator-ci',2)
        recorded('evidence/logs/shaibaan05-calculator-ci-2.txt','shaibaan05-calculator-ci',2,
            'Started by|Checking out Revision|Commit message:|Tests run:|BUILD SUCCESS|CI VERIFIED|Finished:')
    elif index==6:
        recorded('evidence/logs/shaibaan05-calculator-ci-3.txt','shaibaan05-calculator-ci',3,
            'Started by|Commit message:|Tests run:|expected:|BUILD FAILURE|marked build as failure|Skipped archiving|owner notification|Finished:')
    elif index==7:
        recorded('evidence/logs/shaibaan05-calculator-ci-4.txt','shaibaan05-calculator-ci',4,
            'Started by|Commit message:|Tests run:|BUILD SUCCESS|Archiving artifacts|Triggering a new build|owner notification|Finished:')
    elif index==8:
        register=json.loads((ROOT/'evidence/run-register.json').read_text())['runs']
        matches=[r for r in register if r['job']=='shaibaan05-release-sim' and any(c.get('upstreamBuild')==4 for c in r['causes'])]
        selected=matches[0];number=selected['build']
        print('Recorded upstream cause: '+selected['causes'][0]['shortDescription'])
        recorded(f'evidence/logs/shaibaan05-release-sim-{number}.txt','shaibaan05-release-sim',number)
    else:
        recorded('evidence/release-gate.json','shaibaan05-calculator-ci',3)
    print('\nNative screenshot of this terminal only; no password prompts are included.',flush=True)
    time.sleep(1)
    capture(f'T{index:02d}-{name}.png')
print('Nine fresh 05Shaibaan terminal captures complete. Press Enter to close.',flush=True)
input()
