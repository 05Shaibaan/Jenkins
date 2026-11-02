// New-job-only listener. It never reads or changes Jenkins's shared Mailer settings.
import hudson.model.Run
import hudson.model.Result
import hudson.model.TaskListener
import hudson.model.listeners.RunListener
import com.cloudbees.plugins.credentials.CredentialsProvider
import com.cloudbees.plugins.credentials.common.StandardUsernamePasswordCredentials
import hudson.security.ACL
import jakarta.mail.*
import jakarta.mail.internet.*
import java.time.Instant

class Shaibaan05MailListener extends RunListener<Run> {
    Shaibaan05MailListener() { super(Run.class) }
    @Override void onCompleted(Run run, TaskListener listener) {
        if (run.parent.fullName != 'shaibaan05-calculator-ci') return
        def previous=run.previousCompletedBuild
        def failed=run.result==Result.FAILURE || run.result==Result.UNSTABLE
        def recovered=run.result==Result.SUCCESS && previous!=null && previous.result!=Result.SUCCESS
        if (!failed && !recovered) return
        def event=failed?'FAILURE':'RECOVERY'
        try {
            def credential=CredentialsProvider.lookupCredentialsInItem(
                StandardUsernamePasswordCredentials.class, run.parent, ACL.SYSTEM2, [])
                .find{it.id=='shaibaan05-owner-smtp'}
            if (credential==null) throw new IllegalStateException('Owner SMTP credential is not configured')
            def properties=new Properties()
            properties.setProperty('mail.smtp.host','smtp.gmail.com')
            properties.setProperty('mail.smtp.port','465')
            properties.setProperty('mail.smtp.ssl.enable','true')
            properties.setProperty('mail.smtp.auth','true')
            properties.setProperty('mail.smtp.connectiontimeout','15000')
            properties.setProperty('mail.smtp.timeout','15000')
            def mailSession=Session.getInstance(properties, new Authenticator() {
                protected PasswordAuthentication getPasswordAuthentication() {
                    new PasswordAuthentication(credential.username,credential.password.plainText)
                }
            })
            def message=new MimeMessage(mailSession)
            message.setFrom(new InternetAddress(credential.username))
            message.setRecipients(Message.RecipientType.TO,credential.username)
            message.setSubject('[05Shaibaan] '+event+' — '+run.parent.name+' #'+run.number)
            message.setText('Independent 05Shaibaan lab.\nResult: '+run.result+'\nBuild: '+run.number+'\nhttp://localhost:8080/'+run.url+'\nDeployment is simulated and gated on SUCCESS.')
            Transport.send(message)
            def status=Instant.now().toString()+' '+event+' SMTP_ACCEPTED'
            listener.logger.println('[05Shaibaan owner notification] '+status)
            new File(run.rootDir,'shaibaan05-notification.txt').text=status+'\n'
        } catch (Exception error) {
            listener.logger.println('[05Shaibaan owner notification] '+event+' SMTP_FAILED: '+error.class.simpleName)
            new File(run.rootDir,'shaibaan05-notification.txt').text=Instant.now().toString()+' '+event+' SMTP_FAILED '+error.class.simpleName+'\n'
        }
    }
}

def existing=RunListener.all().findAll{it.class.simpleName=='Shaibaan05MailListener'}
existing.each{RunListener.all().remove(it)}
RunListener.all().add(new Shaibaan05MailListener())
println('05Shaibaan-only failure/recovery listener active; shared Mailer configuration untouched.')
