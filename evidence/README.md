# Evidence register · 05Shaibaan

All results below were freshly executed for this repository and its three `shaibaan05-` jobs. No screenshot, test result or build log from EmaadMirza's jobs is reused. Website and native-terminal screenshots are together in [screenshots/](screenshots/).

## Build / break / recover

| New CI run | Commit | Genuine result | Proof |
| --- | --- | --- | --- |
| #1 | `1085aa2` | Manual baseline: two tests pass; executable JAR archived; release #2 triggered | [console](logs/shaibaan05-calculator-ci-1.txt), [build page](screenshots/S02-calculator-first-build.png), [two tests](screenshots/S03-two-signed-tests.png) |
| #2 | `1c8e2a9` | Automatic SCM change; two tests pass; release #4 triggered | [polling log](scm-detection-build-2.txt), [console](logs/shaibaan05-calculator-ci-2.txt), [automatic cause](screenshots/S08-automatic-scm-change.png) |
| #3 | `fc25212` | Automatic intentional failure: expected +11, actual -11; one of two tests fails; no artifact or release; owner failure email accepted | [console](logs/shaibaan05-calculator-ci-3.txt), [failed assertion](screenshots/S11-intentional-sign-failure.png), [failed build](screenshots/S12-failed-build-no-release.png), [gate check](release-gate.json), [SMTP event](owner-notification-3.txt) |
| #4 | `7cd7c7d` | Automatic repair: two tests pass; JAR archived; recovery email accepted; release #5 resumes | [console](logs/shaibaan05-calculator-ci-4.txt), [recovery page](screenshots/S13-recovery-and-artifact.png), [two tests](screenshots/S14-recovery-two-tests.png), [summary](recovery-summary.json), [SMTP event](owner-notification-4.txt) |

The [run register](run-register.json) records actual Jenkins causes, artifact names and test counts. SCM-triggered runs were not started with Build Now. The final configured polling schedule is `H/5 * * * *`; one-minute polling accelerated the fresh verification sequence.

## Welcome and release rehearsal

| New job/run | Observation | Screenshot/log |
| --- | --- | --- |
| Welcome #1 and #2 | Both succeed; greeting identifies 05Shaibaan and the new job | [website](screenshots/S01-welcome-success.png), [#1 output](logs/shaibaan05-welcome-1.txt), [#2 output](logs/shaibaan05-welcome-2.txt) |
| Release #1 | Manual staging, version `1.1.0-rc1`, smoke checks enabled | [console](screenshots/S04-staging-rehearsal.png), [parameters](screenshots/S05-staging-parameters.png) |
| Release #2 | Automatically triggered by successful CI #1 | [upstream cause](screenshots/S06-successful-upstream-release.png), [run JSON](logs/shaibaan05-release-sim-2.json) |
| Release #3 | Manual production simulation, smoke checks disabled | [console](screenshots/S07-production-smoke-skipped.png) |
| Release #4 | Automatically triggered by successful CI #2 | [output](logs/shaibaan05-release-sim-4.txt) |
| No release from failed CI #3 | Last deployment remains #4 before and after failure | [recorded gate](release-gate.json), [terminal proof](screenshots/T09-release-gate.png) |
| Release #5 | Automatically triggered by recovered CI #4; dev / 1.1.0 / smoke=true | [resumed release](screenshots/S15-resumed-release.png), [output](logs/shaibaan05-release-sim-5.txt) |

Deployments and smoke checks are explicitly simulated. They change no remote server.

## Actual Ubuntu terminal captures

The cyan workshop heading is output inside a real GNOME Terminal. Ubuntu's native screenshot portal captured its pixels. Only the evidence monitor is retained using a lossless crop; full-desktop originals remain private under ignored `.lab/raw-terminal/`. No terminal image/text was rendered or fabricated. [Capture/session record](terminal-session.json) includes hashes and crop bounds. Historical output is explicitly labelled with its new job/build number and **saved output from earlier run**.

| Capture | What it shows |
| --- | --- |
| [T01 · reused runtime](screenshots/T01-runtime.png) | Live Ubuntu, Java/Javac, Git, Maven, Jenkins service/version and local Git author |
| [T02 · welcome](screenshots/T02-welcome.png) | Saved output from this lab's Welcome #1 |
| [T03 · fresh Maven](screenshots/T03-fresh-maven.png) | A new offline `clean package`, exactly two passing signed-arithmetic tests and BUILD SUCCESS |
| [T04 · JAR execution](screenshots/T04-jar-execution.png) | Freshly generated JAR listed, hashed and executed |
| [T05 · SCM detection](screenshots/T05-scm-detection.png) | New-repository commit detected by polling; this lab's automatic CI #2 |
| [T06 · intentional failure](screenshots/T06-failure.png) | This lab's CI #3, sign mismatch, Jenkins FAILURE and owner SMTP acceptance |
| [T07 · recovery](screenshots/T07-recovery.png) | This lab's CI #4, two passing tests, archive, resumed downstream and recovery SMTP acceptance |
| [T08 · release](screenshots/T08-release.png) | This lab's release #5, successful upstream cause, environment/version and smoke output |
| [T09 · safety gate](screenshots/T09-release-gate.png) | Actual failed-run gate snapshot: release count unchanged and no archived artifact |

## Configuration, artifact and account isolation

- [Configuration screenshot](screenshots/S10-ci-config-snapshot.png): the real configuration snapshot archived by CI #2 and viewed as text through Jenkins; this is not an admin-form screenshot. It shows SCM, verification-time polling, tools, publishers and wrappers. [Current exported XML](../jenkins/shaibaan05-calculator-ci.xml) contains the final five-minute schedule.
- [Archived artifact website](screenshots/S09-archived-executable-jar.png); [actual CI #4 executable JAR](artifact/shaibaan-calculator-1.1.0.jar) and [SHA-256](artifact/SHA256SUMS).
- [Owner authentication audit](owner-access.json): verified GitHub identity and push permission; contains no token.
- [Owner notification audit](notifications.json): new encrypted credential ID, failure/recovery SMTP acceptance, and no use of the shared Mailer account. Inbox receipt is not independently verified or claimed.
- [Preservation audit](preservation-check.json): existing tracked files, jobs, history and global Mailer configuration remain unchanged.
- [Reused infrastructure and PDF source](infrastructure.json): versions, cache/setup reuse, original instruction hash and disk space. The fresh apt/wizard steps were intentionally not repeated, as requested. No private-repository checkout, production deployment, inbox screenshot or new Jenkins installation is claimed.

All helper code/templates and capture technology reused from the earlier setup are identified in the README. Every result/image here belongs to the new account's executions. Files containing credentials, the Jenkins home, tools, dependency cache, target directory and rejected/raw captures are excluded from Git.
