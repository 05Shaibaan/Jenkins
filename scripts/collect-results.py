#!/usr/bin/env python3
"""Collect only this lab's new jobs through the authorized local Jenkins admin session."""
from pathlib import Path
import datetime
import json
import re
import jenkins_admin as admin

root=Path(__file__).resolve().parents[1]
jobs=['shaibaan05-welcome','shaibaan05-calculator-ci','shaibaan05-release-sim']
summary=[]
for job in jobs:
    data=admin.get('job/'+job+'/api/json').json()
    for item in data['builds']:
        number=item['number']
        result=admin.get(f'job/{job}/{number}/api/json').json()
        if result['building']:continue
        base=root/'evidence/logs'/f'{job}-{number}'
        console=admin.get(f'job/{job}/{number}/consoleText').text
        console=re.sub(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}','[owner-recipient]',console)
        base.with_suffix('.txt').write_text(console)
        base.with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
        record={'job':job,'build':number,'result':result['result'],
                'causes':[cause for action in result['actions'] for cause in action.get('causes',[])],
                'artifacts':[artifact['fileName'] for artifact in result['artifacts']]}
        if job=='shaibaan05-calculator-ci':
            tests=admin.get(f'job/{job}/{number}/testReport/api/json').json()
            (root/'evidence'/f'calculator-tests-{number}.json').write_text(json.dumps(tests,indent=2)+'\n')
            record.update({'passed':tests['passCount'],'failed':tests['failCount'],'skipped':tests['skipCount']})
            notification=Path('/home/mirza/jenkins-assignment/.lab/jenkins-home/jobs')/job/'builds'/str(number)/'shaibaan05-notification.txt'
            if notification.exists():
                (root/'evidence'/f'owner-notification-{number}.txt').write_text(notification.read_text())
                record['ownerNotification']=notification.read_text().strip()
        summary.append(record)
(root/'evidence/run-register.json').write_text(json.dumps({'captured':datetime.datetime.now().astimezone().isoformat(),'runs':summary},indent=2)+'\n')
print('Collected',len(summary),'fresh runs from 05Shaibaan-prefixed jobs only.')
