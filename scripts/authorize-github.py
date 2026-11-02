#!/usr/bin/env python3
"""Authorize ONLY this local repository. Enter the owner token locally, never in chat."""
import getpass
import json
import pathlib
import subprocess
import urllib.error
import urllib.request

root=pathlib.Path(__file__).resolve().parents[1]
token=getpass.getpass('05Shaibaan GitHub token (hidden; only Jenkins repository Contents read/write): ').strip()
if not token:raise SystemExit('No token entered; nothing changed.')
def api(path):
    request=urllib.request.Request('https://api.github.com/'+path,
        headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','User-Agent':'shaibaan05-lab'})
    with urllib.request.urlopen(request,timeout=30) as response:return json.load(response)
try:
    identity=api('user')
    if identity['login'].lower()!='05shaibaan':raise SystemExit('Wrong GitHub account. Nothing saved.')
    repo=api('repos/05Shaibaan/Jenkins')
    if not repo.get('permissions',{}).get('push'):raise SystemExit('This token lacks repository write permission. Nothing saved.')
except urllib.error.HTTPError as error:
    raise SystemExit('GitHub authorization failed (HTTP '+str(error.code)+'). Check token access locally.')
private=root/'.lab';private.mkdir(exist_ok=True)
credential=private/'github-owner.credentials'
credential.touch(mode=0o600,exist_ok=True);credential.chmod(0o600)
credential.write_text('https://05Shaibaan:'+token+'@github.com/05Shaibaan/Jenkins.git\n')
subprocess.run(['git','-C',str(root),'config','--local','credential.useHttpPath','true'],check=True)
subprocess.run(['git','-C',str(root),'config','--local','--replace-all','credential.helper',''],check=True)
subprocess.run(['git','-C',str(root),'config','--local','--add','credential.helper','store --file='+str(credential)],check=True)
(private/'github-ready.json').write_text(json.dumps({'login':identity['login'],'repository':repo['full_name'],'push':True})+'\n')
token=None
print('Verified 05Shaibaan with write permission on 05Shaibaan/Jenkins. Only this repository uses the isolated credential file.')
