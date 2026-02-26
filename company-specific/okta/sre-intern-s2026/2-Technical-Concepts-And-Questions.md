# **Technical SRE Concepts - Specific to Resume**

---

## ForOurLastNames: AWS Lambda & Serverless
*Resume states:* - deployed a containerized Node app with Lambda, API Gateway, S3, CloudFront.

1. What is a cold start in Lambda? Why does it happen?  
2. How would you reduce cold start latency?  
3. What are tradeoffs between Lambda and EC2?  
4. How does API Gateway integrate with Lambda?  
5. How do you handle retries in serverless systems?  
6. How does horizontal scaling work in Lambda?  
7. What limits does Lambda have?  

SRE-specific:  
1. What happens if Lambda starts throttling?  
2. How do you monitor Lambda reliability?  

---

## ForOurLastNames: Observability  
*Resume states:* Deployment monitoring using Prometheus/Grafana with Cloudwatch Exporter metrics  

1. What are the 3 pillars of observability?  
2. Difference between metrics, logs, and traces?  
3. What is latency vs throughput?  
4. What is P95 vs average?  
5. How do you detect a memory leak?  
6. What is an SLO?  
7. What is error budget?  

SRE-specific:  
1. If API latency spikes from 200ms to 800ms, how would you debug it?  

---

## ForOurLastNames: Authentication & Webhooks  
*Resume states*: used Supabase Auth with RLS, implemented Stripe payment system using webhooks, ensuring idempotency  

1. What is idempotency?  
2. Why are webhooks dangerous?  
3. What happens if Stripe sends the same event twice?  
4. How do you secure a webhook endpoint?  
5. What is row-level security?  
6. What is JWT?  
7. What is OAuth?  
8. Difference between authentication and authorization?  
9. What is SSO?  
10. What is an access token vs refresh token?  

---

## PM Accelerator: Asynchronous Systems (Celery + Redis)  
*Resume states:* created a asynchronous task queue system using Celery and Redis  

1. What problem does Celery solve?  
2. Why use Redis as a broker?  
3. What happens if a worker crashes mid-task?  
4. How do you ensure tasks aren’t lost?  
5. What is eventual consistency?  

SRE-specific:  
1. How do you monitor queue backlog?  
2. What happens if Redis goes down?  

---

## Trace: SSH Automation  
*Resume states:* automated diagnostics across 1,000+ devices via SSH.  

1. What is SSH?  
2. What happens if a device is unreachable?  
3. How would you parallelize device checks?  
4. How would you prevent overwhelming devices?  
5. How would you retry safely?  

---

## Additional SRE Questions  
1. What is high availability?  
2. What is the difference between reliability and availability?  
3. What is a postmortem?  
4. What is incident response?  
5. What is MTTR?  
6. What is a runbook?  
7. What is load shedding?  
8. What is rate limiting?  
9. What is exponential backoff?  
10. What happens during a cascading failure?  

# **Questions After Technical**

1. In your experience, what kinds of manual operational work have you been able to eliminate through automation?

2. How does working across multiple cloud providers affect reliability strategies? Does it make things more complex, or are they similar enough to be somewhat generalized and redundant?

3. How do engineers collaborate, and what kind of internal tools does Okta lean towards to help in productivity and collaboration between supporting engineers?

4. What incidents happen in high-compliance environments, how does that change current practices in observability and such?

5. For someone early in their career interested in backend infrastructure and reliability, what skills and/or habits make the biggest difference in how well they do within the team?

6. I saw Okta operates at FedRAMP High, how does that change the way site reliability engineering works compared to commercial or personal usage environments?
