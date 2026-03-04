# Okta Behavioral Interview Preparation

Compilation of STAR stories + topics to focus in on specific to Okta SRE intern role descriptions.

---

## Ownership

1. Tell me about a time you owned something end-to-end.

2. Tell me about a time something broke.

3. Tell me about a mistake you made.

Topics to talk about:
- Lambda production deployment
- Webhook idempotency handling
- SSH automation across 1,000+ devices
- Celery async architecture

---

## Reliability & Incident Thinking (SRE-specific)

1. Tell me about a production issue.

2. How do you respond when something is down?

3. Have you ever had to debug under pressure?

4. How do you balance speed vs reliability?

Topics to talk about:
- Remote diagnostics + hardware troubleshooting
- Observability dashboards for Lambda
- Webhook replay/idempotency protection

Focus on:
- Structured thinking
- Calmness
- Communication
- Preventative improvement after

---

## Handling Ambiguity

1. Tell me about a time requirements were unclear.

2. How do you approach open-ended problems?

3. How do you prioritize when everything feels urgent?


Topics to talk about:
- Designing AWS infra yourself
- Designing observability dashboards
- Building async Celery system

---

## STORY 1 — Production Deployment (Ownership + Systems)

**Characteristics/Traits Demonstrated:**
- Ownership
- Technical leadership
- Ambiguity
- Scaling

**Emphasize:**
1. Why you chose serverless
2. Cold start tradeoffs
3. Monitoring decisions
4. Capacity planning
5. Overall design of infra for deployment

---

## STORY 2 — Webhook Idempotency (Reliability Mindset)

**Characteristics/Traits Demonstrated:**
- Reliability engineering
- Defensive system design
- Anticipating failure cases
- Distributed systems awareness

**Emphasize:**
1. Why duplicate webhooks are dangerous
2. Stripe may retry events on network failure
3. Without protection → double billing / inconsistent subscription state
4. How you enforced idempotency through stored event IDs
6. Checked processed events before applying state changes
7. Ensured subscription updates only applied once
8. Protected against race conditions and retries
9. Maintained consistent user subscription state
10. Security considerations
11. Verified webhook signatures + Prevented malicious requests

---

## STORY 3 — SSH Automation & Device Debugging (Operational Reliability)

**Characteristics/Traits Demonstrated:**
- Incident response
- Reliability at scale
- Operational automation
- Systems troubleshooting


**Emphasize:**
1. The operational problem
2. Hardware devices frequently needed diagnostics
3. Engineers manually SSH’d into devices
4. Troubleshooting was slow and inconsistent
5. How you automated it
6. Built Python scripts using SSH (Paramiko)

---

## STORY 4 — Celery + Redis Async Processing (Scalability)

**Characteristics/Traits Demonstrated:**
- Systems optimization
- Performance improvement
- Scalability thinking
- Architecture design


**Emphasize:**
1. Performance bottleneck(s)
2. Converted processing pipeline into asynchronous tasks
3. Parallelization benefits
4. Tasks distributed across multiple workers
5. Allowed concurrent document processing


---

## STORY 5 — Observability Dashboards (SRE Mindset)

**Characteristics/Traits Demonstrated:**
- Observability design
- Reliability monitoring
- Data-driven operations
- Proactive system management


**Emphasize:**
1. Why observability mattered
2. Serverless systems scale automatically
3. Without monitoring, performance issues are hard to detect
4. Metrics you tracked
6. Lambda invocation counts
7. Cold start frequency
8. Memory utilization
9. API latency


---

## STORY 6 — A Failure / Learning Experience

**Characteristics/Traits Demonstrated:**
- Ownership
- Accountability
- Learning from mistakes
- Continuous improvement


**Emphasize:**
1. Initial webhook logic did not account for repeated event delivery
2. Duplicate events caused inconsistent state updates
3. How you diagnosed it through investigated logs
4. Observed duplicate webhook deliveries from Stripe retries
5. Implemented idempotency checks
6. Ensured repeated events would not reapply state changes


---

# Mock Questions

Use STAR format (Situation, Task, Action, Result) to answer the following:

1. Tell me about a time something broke in production. What did you do?

2. Tell me about a time you had to make a tradeoff between moving fast and building something reliable.

3. How do you respond when you don’t know how to solve a problem?

4. Tell me about a time you automated something manually painful.

5. What does reliability mean to you?


## SRE-Specific Behavioral Questions They May Ask

1. How do you stay calm during incidents?

2. How would you communicate during an outage?

3. Have you ever disagreed with an architectural decision?

4. What is more important: uptime or feature velocity?

5. How do you prevent the same issue from happening twice?