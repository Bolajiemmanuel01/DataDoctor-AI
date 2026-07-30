# Security Playbook

Purpose: provide a concrete, actionable runbook for responding to security incidents affecting DataDoctor AI (POC and production).

This playbook is scoped to common classes of incidents relevant to this project: leaked credentials, data exfiltration, unauthorized access, compromised jobs or worker nodes, and data integrity incidents.

--

1) Roles & responsibilities

- Incident Lead: coordinates response, owns communications and timeline.
- Engineering Lead: executes containment, remediation, and recovery steps.
- Security/Compliance Lead: assesses regulatory obligations and notifies authorities where required.
- Communications Lead: drafts internal and external messages (legal review where necessary).
- On-call DevOps: manages infrastructure controls (rotate keys, isolate networks).

2) Severity levels

- Sev-1 (Critical): confirmed data exfiltration of production customer data, active exploitation, or production downtime affecting all tenants.
- Sev-2 (High): unauthorized access to a limited set of data, worker compromise, or sensitive secret exposure.
- Sev-3 (Medium): non-production incidents, failed logins, anomalous jobs without confirmed data loss.
- Sev-4 (Low): informational findings, suspicious log entries without corroborating evidence.

3) Initial detection & triage (first 60 minutes)

- Triage: Incident Lead validates the alert and assigns severity.
- Capture timeline: record first-detected timestamp, alert source, affected services, and initial indicators of compromise (IoCs).
- Short-term containment: depending on severity, take one or more of these actions:
  - Revoke/rotate exposed credentials (API keys, service accounts).
  - Suspend affected worker queues or pause job ingestion.
  - Block suspicious IP addresses at perimeter (WAF/Firewall).
  - Isolate affected hosts (remove from LB, stop containers).
- Preserve evidence: snapshot logs, DB transaction logs, application server memory if feasible, and keep copies of artifacts in a secure location for forensic analysis.

4) Investigation

- Collect relevant logs (application, worker, broker, DB, object storage access logs).
- Identify root cause (vulnerability, stolen credentials, misconfiguration, compromised dependency).
- Determine scope: which datasets, jobs, user accounts, and time window are impacted.

5) Containment, eradication, recovery

- Containment: remove attacker access, close vulnerable vectors, isolate compromised hosts.
- Eradication: patch vulnerability, rotate secrets, remove malicious artifacts.
- Recovery: restore services from verified backups, re-run ingestion/processing if needed, validate data integrity.
- Validation: run end-to-end tests and smoke tests; validate job outputs and sampling of cleaned artifacts.

6) Customer & regulator communication

- Internal notification: inform leadership, legal, and affected engineering teams within the SLAs defined by Severity.
- External notification: follow regulatory timelines; for GDPR, notify supervisory authority within 72 hours when personal data breach exists.
- Customer communication: notify affected customers with clear description of impact, remediation steps, and mitigation guidance; provide contact for support.

7) Post-incident review

- Conduct a blameless post-mortem documenting timeline, root cause, actions taken, gaps, and follow-up items.
- Track remediation tasks with owners and due dates; verify closure in follow-up review.

8) Runbooks (quick actions)

- Compromised credential (API key or DB password):
  1. Revoke the credential immediately.
  2. Rotate to a new credential and update services.
  3. Search logs for usage of the old credential and determine affected resources.

- Data exfiltration suspected:
  1. Isolate the storage bucket or block read access.
  2. Dump ACLs and access logs for the period of concern.
  3. Notify Incident Lead and Legal.

- Malicious job or worker behavior:
  1. Stop the relevant worker pool.
  2. Take container images offline and inspect image history.
  3. Rebuild workers from trusted images and re-deploy.

9) Forensics & evidence handling

- Preserve original logs and artifacts; do not modify them in place.
- Use checksums and chain-of-custody records when transferring evidence to external teams.

10) Preventive controls (recommendations)

- Enforce strong secret management (vaults), short-lived credentials, and least privilege for service accounts.
- Protect object storage with bucket policies and signed URLs only.
- Enable multi-factor auth (MFA) for all accounts with elevated privileges.
- Harden container images (minimal base images, vulnerability scanning) and run periodic dependency scans.
- Apply input validation and safe-parsing libraries to avoid CSV/Excel injection attacks.

11) Playbook testing

- Conduct regular tabletop exercises and simulate incident scenarios.
- Run chaos tests for worker and queue failures and ensure graceful degradation.

12) Contact templates (examples)

- Internal alert template: include incident id, severity, short description, initial containment steps, and requested immediate actions.
- Customer notification template: include what happened, what data was impacted, what we did, recommended customer actions, and contact.

--

Keep this file updated as the platform evolves from POC to production — new services, storage backends, and identity providers should be reflected here.
