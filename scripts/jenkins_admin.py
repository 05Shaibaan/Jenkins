"""Local authorized administrator session. No secret is copied into repository files."""
from pathlib import Path
import os
import requests

BASE=os.environ.get('JENKINS_URL','http://127.0.0.1:8080/').rstrip('/')+'/'
secret_file=Path(os.environ.get('JENKINS_ADMIN_SECRET_FILE','/home/mirza/jenkins-assignment/.lab/admin-password'))
session=requests.Session()
session.auth=(os.environ.get('JENKINS_ADMIN_USER','lab-admin'),secret_file.read_text().strip())
r=session.get(BASE+'crumbIssuer/api/json',timeout=15);r.raise_for_status()
c=r.json();session.headers[c['crumbRequestField']]=c['crumb']
def get(path):
    r=session.get(BASE+path,timeout=60);r.raise_for_status();return r
def post(path,**kwargs):
    r=session.post(BASE+path,timeout=120,**kwargs);r.raise_for_status();return r
