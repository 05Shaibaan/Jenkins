# 05Shaibaan · Signed Arithmetic Delivery Workshop

An independent Jenkins lab for **[05Shaibaan/Jenkins](https://github.com/05Shaibaan/Jenkins)**: test signed arithmetic, rehearse releases, deliberately break a sign, and recover safely.

## The delivery route

| Stage | New freestyle job | What it proves |
| --- | --- | --- |
| Welcome | `shaibaan05-welcome` | Fresh greeting, build identity, Ubuntu execution user and timestamp |
| Verify | `shaibaan05-calculator-ci` | GitHub polling → Maven → exactly two tests → executable JAR, JUnit results and archive |
| Rehearse | `shaibaan05-release-sim` | Parameterized deployment simulation; automated releases require upstream SUCCESS |

This version uses package `dev.shaibaan.calculator`, artifact `shaibaan-calculator-1.1.0.jar`, negative operands, and tests `addsPositiveAndNegativeOperands` and `subtractsAcrossZero`. Release parameters are `TARGET_ENV`, `RELEASE_VERSION`, and `RUN_SMOKE_TESTS`; staging uses release `1.1.0-rc1`. These are new source files, jobs, commits and executions—not renamed results from another account.

## Results and evidence

See the [evidence register](evidence/README.md) for the exact builds, commit IDs, screenshots and mail status. All screenshots—website and real Ubuntu terminal—are together in [evidence/screenshots/](evidence/screenshots/). Historical output displayed in Terminal names the actual new job/build and says **saved output from earlier run**.

The deliberate failure changes the subtraction assertion from `-11` to `+11`; the repair restores the sign. Failed builds publish their test failure but archive no artifact and trigger no release. The smoke tests and deployments are simulations; no remote application server is modified.

## Reuse without reinstalling

The original 23-page `Jenkins.pdf` was read before this lab. Java 21, Git, Jenkins 2.580.2, Maven 3.9.16, the existing plugins and the 25 MiB Maven cache are reused on this Ubuntu machine. No new Jenkins installation, plugin installation, package download or dependency download was needed. Maven runs with `-o` to enforce offline reuse.

Shared paths are `/home/mirza/jenkins-assignment/.lab/tools/apache-maven-3.9.16`, `/home/mirza/jenkins-assignment/.lab/m2`, and the running localhost-only `jenkins-assignment` user service. The Jenkins home naturally stores the new prefixed jobs, but the original jobs, Git repository, tracked evidence and global Mailer settings remain unchanged. A preservation audit records their hashes. Provisioning/XML and native capture techniques reuse the earlier lab's templates/tools; no earlier build log, result or screenshot is used as 05Shaibaan evidence.

The PDF's fresh apt installation, unlock wizard and public firewall setup are reused infrastructure rather than repeated exercises. This user-specified repository is public, so Jenkins SCM checkout is anonymous. The owner's separate fine-grained token is used only to push to this repository. No private-repository PAT checkout is claimed.

## Reproduce locally

```bash
cd ~/jenkins-05shaibaan
/home/mirza/jenkins-assignment/.lab/tools/apache-maven-3.9.16/bin/mvn \
  -o -B -ntp -Dmaven.repo.local=/home/mirza/jenkins-assignment/.lab/m2 clean package
java -jar target/shaibaan-calculator-1.1.0.jar
```

The JAR prints both `12 + (-7) = 5` and `-3 - 8 = -11`. Surefire XML is in `target/surefire-reports/`.

To provision missing jobs on the reused instance, run `python3 scripts/provision-jobs.py` from an authorized local admin session. It preserves any existing job and registers only the 05Shaibaan mail listener. The shared tool names must be `JDK-21` and `Maven-3.9`. To use another authorized admin session, set `JENKINS_ADMIN_USER` and `JENKINS_ADMIN_SECRET_FILE` locally; never put the secret in an argument or commit it.

The new jobs have workspace cleanup, timestamps, a ten-minute timeout, ten-build retention, JUnit publishing and success-only artifact archival/chaining. The final polling schedule is documented in the job XML; faster one-minute polling is used during the verification exercise.

## Owner-only authentication and email

Local Git author settings identify Syed Shaibaan Hussain (`86466077+05Shaibaan@users.noreply.github.com`). Authentication was verified as **05Shaibaan**, with push permission, before writing. A repository-local credential helper isolates the owner's token in ignored `.lab/`; no global Git settings or existing Git credentials are overwritten, and no collaborator is added.

For independent Gmail notifications, run `python3 scripts/configure-owner-email.py` locally and enter the owner's Gmail address and App Password at the hidden prompt. The new encrypted credential ID is `shaibaan05-owner-smtp`. A job-filtered [notification listener](jenkins/owner-notifications.groovy) sends failure/recovery messages using only that ID; it never reads or changes the shared Mailer account. It must be registered again with the provisioning script after a Jenkins restart. This isolates accounts without adding plugins or restarting the shared instance.

Logs record SMTP acceptance separately from any recipient inbox confirmation. No password, token, full Jenkins home, binary tool, cache or unrelated file belongs in Git. `.lab/`, `target/` and credential files are excluded. Native terminal captures keep any unrelated monitor private and publish only the inspected terminal pixels.
