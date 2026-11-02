#!/usr/bin/env python3
"""Enter the 05Shaibaan owner's Gmail App Password locally; no shared email secrets used."""
import getpass
import json
from pathlib import Path
import jenkins_admin as admin

root=Path(__file__).resolve().parents[1]
address=input('05Shaibaan owner Gmail address: ').strip()
password=getpass.getpass('This owner\'s Gmail App Password (hidden): ').replace(' ','')
if not password or '@' not in address:raise SystemExit('Missing address/app password; nothing saved.')
script='''
import jenkins.model.Jenkins
import com.cloudbees.plugins.credentials.*
import com.cloudbees.plugins.credentials.domains.Domain
import com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl
def store=SystemCredentialsProvider.getInstance().store
def domain=Domain.global()
def old=store.getCredentials(domain).find{it.id=='shaibaan05-owner-smtp'}
def credential=new UsernamePasswordCredentialsImpl(CredentialsScope.GLOBAL,'shaibaan05-owner-smtp',
    '05Shaibaan owner SMTP — isolated from the shared Mailer account',%s,%s)
if(old!=null)store.updateCredentials(domain,old,credential)
else store.addCredentials(domain,credential)
def properties=new Properties()
properties.setProperty('mail.smtp.host','smtp.gmail.com')
properties.setProperty('mail.smtp.port','465')
properties.setProperty('mail.smtp.ssl.enable','true')
properties.setProperty('mail.smtp.auth','true')
properties.setProperty('mail.smtp.connectiontimeout','15000')
properties.setProperty('mail.smtp.timeout','15000')
def mailSession=jakarta.mail.Session.getInstance(properties,new jakarta.mail.Authenticator(){
    protected jakarta.mail.PasswordAuthentication getPasswordAuthentication(){
        new jakarta.mail.PasswordAuthentication(credential.username,credential.password.plainText)
    }
})
try {
    def message=new jakarta.mail.internet.MimeMessage(mailSession)
    message.setFrom(new jakarta.mail.internet.InternetAddress(credential.username))
    message.setRecipients(jakarta.mail.Message.RecipientType.TO,credential.username)
    message.setSubject('[05Shaibaan] independent Jenkins SMTP test')
    message.setText('This SMTP test uses only the 05Shaibaan owner credential. Existing lab mail settings were not changed.')
    jakarta.mail.Transport.send(message)
    println('OWNER_SMTP_ACCEPTED')
} catch(Exception error) {
    println('OWNER_SMTP_FAILED '+error.class.simpleName)
}
'''%(json.dumps(address),json.dumps(password))
r=admin.post('scriptText',data={'script':script})
password=None;script=None
if 'OWNER_SMTP_ACCEPTED' not in r.text:
    raise SystemExit('Owner SMTP test failed. Check the local App Password/account; no secret was printed.')
(root/'.lab/owner-email-ready').write_text('Owner SMTP configuration test accepted\n')
print('Owner SMTP test accepted. Credential stored encrypted in Jenkins with a separate ID; shared Mailer settings untouched.')
