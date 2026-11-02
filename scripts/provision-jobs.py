#!/usr/bin/env python3
"""Create only missing 05Shaibaan jobs in the existing instance; never overwrite jobs."""
from pathlib import Path
import jenkins_admin as admin

root=Path(__file__).resolve().parents[1]
for name in ['shaibaan05-welcome','shaibaan05-release-sim','shaibaan05-calculator-ci']:
    response=admin.session.get(admin.BASE+'job/'+name+'/api/json',timeout=15)
    if response.status_code==200:
        print('Preserved existing job:',name)
        continue
    if response.status_code!=404:response.raise_for_status()
    content=(root/'jenkins'/f'{name}.xml').read_bytes()
    admin.post('createItem',params={'name':name},data=content,headers={'Content-Type':'application/xml'})
    print('Created:',name)
script=(root/'jenkins/owner-notifications.groovy').read_text()
response=admin.post('scriptText',data={'script':script})
if 'listener active' not in response.text:raise SystemExit('Notification registration failed; inspect locally.')
print('05Shaibaan-only notification listener registered; reapply after a Jenkins restart.')
