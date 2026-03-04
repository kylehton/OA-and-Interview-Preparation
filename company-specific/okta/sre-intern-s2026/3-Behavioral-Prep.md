# Okta Behavioral Interview Preparation

Compilation of STAR stories + topics to focus in on specific to Okta SRE intern role descriptions.

---

## Why Site Reliability Engineering? Why Okta?

Throughout my internships and personal projects, I started realizing that the parts of engineering I enjoyed the most were the ones focused on making systems reliable and trustworthy for real users. For example, when I was building backend services, I found myself thinking not just about whether something worked, but how it behaved in production, things like monitoring, handling retries, or ensuring systems continued working when something failed. At the time, I hadn’t really connected that mindset to the role of Site Reliability Engineering. After learning more about SRE and speaking with previous Okta interns, I realized that many of the problems I naturally gravitated toward, like observability, automation, and designing systems that handle failure gracefully, which are core parts of the SRE role. That’s what excites me about the opportunity at Okta. Identity infrastructure sits on the critical path for so many applications, which means reliability and security are incredibly important. Being able to work on systems where reliability directly impacts millions of users is something I find really exciting, and it’s an environment where I believe I could grow a lot as an engineer.

---

## Ownership

1. Tell me about a time you owned something end-to-end.  
    A time I owned something end to end was during my internship with ForOurLastNames. There were very few technical interns, and I was one of the few on the team. Thus, I was placed in charge of the deployment for the entire FOLN application, from designing the architecture and infrastructure used to deploy the different parts of the application, as well as configuring them to work cohesively together.

2. Tell me about a time that something broke.  
    During a push/merge with changes made from one of the software engineers, the login system broke. I was the first one to notice this, and so I immediately worked on finding the issue. The change was from a refactoring of user data storage in cookies, changed to session storage. Given the deployment did not yet exist, there were no traces or logs to work with, so I ended up tracing the login flow by hand through the functions and files in the codebase. Eventually, I discovered the issue, where there was outdated logic using previous accessors for user data, where it was not accessing user data at the correct location. I was able to fix this, and along with the software engineer, we went through the entire login process and standardized the new changes everywhere, as well as documented it for future migrations or changes.

3. Tell me about a mistake you made.
    During my first internship at Trace, I made the mistake of bulking my changes to the quality assurance testing script. Instead of making smaller changes and testing them to ensure validity and correctness, I added all my changes then ran them directly on the troubleshooting cameras. With that, I ended up receiving invalid logs across the board for those cameras, and had to then manually test them outside using the manual testing script. Afterwards, my mentor and I went back through and reviewed my changes to the script. Luckily, the script itself was changed only on the local machine I was working on, and we were able to correct the issues and resolve a working version. From this experience, I learned the importance of iterating slowly and being more deliberate and careful. Had my changes been to something in production with users, the impact would have been far greater.

Topics to talk about:
- Lambda production deployment
- Webhook idempotency handling
- SSH automation across 1,000+ devices
- Celery async architecture

---

## Reliability & Incident Thinking (SRE-specific)

Preface: I have never worked in a production environment, so these answers are conceptual and hypothetical, not yet backed by experience.

1. How do you respond when something is down?
    I would first triage the issue to ensure minimal impact to users. This could be in the form of rollbacks, shutdowns, and things of that nature in accordance to the critical nature of the issue. Then, I would check metrics to view the area of effect the issue has, whether it is a single instance issue, or widespread across regions/deployments. I would then dig deeper through using traces, finding the area(s) that are causing this, and pinpoint the exact problems using the function/logic logs.

2. Have you ever had to debug under pressure?
    I have never had to debug under pressure or in production, however, I do treat debugging in all environments as if I was in production, to build strong habits and structure in my debugging. I believe being methodical and iterative is the best way to debug under pressure, and using a sort of checklist and structure to debugging is how I do that. I generally mock up a list of potential issues I believe I should investigate, based on metrics. From there, I look into traces and logs and rule out invalid options, and explore deeper into viable issues that may be the actual cause, and add any additional issues that I believe could be a possibility. I essentially funnel wide and get narrower as I debug, in order to be efficient in debugging in cases where my first few attempts may be incorrect.

3. How do you balance speed vs reliability?
    I believe that if one is placed above the other, reliability should be more important than speed. With that in mind, I always lean towards reliability, especially for critical functions and applications. Tradeoffs for speed can be made in noncritical areas, where reliability may not be as necessary. However, in my opinion, there is no use in being efficient and fast if you are inconsistent and unreliable.

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

1. Tell me about a time that requirements were unclear.
    One time my requirements were unclear was during my deployment project at ForOurLastNames. The team had finished iterating their beta version of the application and wanted to deploy the app, which is what I was assigned to do. The instructions I was given were to find the best way to deploy the application for the company. I had no other guidance or requirements other than that, and so it was vague from the start. The first thing I did was research many of the deployment options out there, for database, front-end, and server, and compile them. From this, I wrote up detailed descriptions of each, highlighting tradeoffs that would need to be made, especially revolving around server-side deployment. The team wanted their stack configured around AWS, so I chose to pursue those options. I met frequently with the CEO and CTO, explaining different paths I was considering, such as whether to use AWS Lambda or EC2, and what features we would have to consider for both. Eventually, I was able to come to a conclusive plan for the client-side and server-side deployments, and utilized S3, CloudFront CDN, API Gateway, and Lambda to deploy our single-origin application on AWS. By the end of my internship, I successfully completed my project and got the first initial version of the application up and running for investors and beta-testers to use.

2. How do you approach open-ended problems?
    I approach open-ended problems by clarifying and asking questions to consolidate my understanding of the problem. During my task to implement Stripe payments for subscriptions, I was fully in charge of what data to store in database and what to ignore. At the time, I was new to Stripe API integration and did not yet know what was necessary. From this, I asked more questions and got a better understanding of what the CTO had in mind. From that, I stored specific data for checks of subscription, trials, and for user database logging. 

3. How do you prioritize when everything feels urgent?
    I prioritize based on user impact. I believe the tasks with the most effect should be completed first, to ensure a good user experience and minimalization of issues and problems that may occur. With that, it is also important to be structured in pressured and urgent settings to stay on track and work methodically.


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

During my time at ForOurLastNames, I was hired as a full-stack software engineering intern, specifically for my previous project experience with AWS and hosting. As such, the team was nearly ready to launch their application to investors and beta-testers, and wanted to deploy it. I was tasked with approaching deployments for the entire application. The requirements given to me where quite loose and pretty vague, so I was essentially starting from a blank slate. I did lots of research on various services, like AWS, GCP, and Azure, as well as smaller deployment sites like Heroku and Railway. I ended up compiling a spreadsheet of services I believed would be applicable, and presented that to the CEO and CTO. We eventually came to the conclusion to use Lambda as the server-side deployment. Given that the client-side of the application was an SPA (Single Page Application), where each page is precompiled then filled in with specified information, I chose to also use a serverless deployment for that. As such, we decided to use S3 and CloudFront to host the SPA in conjunction with API Gateway and Lambda. From here, we built a single origin application, routed via CloudFront to either the built React pages or to the function gateway. A big component in the decision to go serverless was cost. Given that this initial launch would be exclusively for investors and beta-testers, speed was not high in priority for the CEO and CTO. Additionally, the function itself was not very large, so cold start latency was not very significant. In the end, I were able to deploy the application as well as document the process for future interns.

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
11. Verified webhook signatures + prevented malicious requests

Halfway through my internship at ForOurLastNames, I was tasked with implementing Stripe subscriptions for the application. Given that this was my first experience working with Stripe API and payments, I researched on their subscriptions system and decided on implementing Stripe's consumer API endpoint and webhooks for database event updates. I was able to get a working version, however, through manual testing, I realized that duplicate webhooks were still being processed individually and that it could cause wrongful updates to the state of the user subscription and such. From there, I researched on common methods companies used to ensure idempotency through Stripe subscriptions, and began using event ids as a precheck for event processing. This ensured truthful protection under retries and race conditions, and duplicate events. Of course, given the dangerous nature of webhooks being an HTTP request, in order to secure the reception and usage of the webhook and its data, I utilized Stripe's built-in signature, ensuring that it could not be accessed by any interceptions, and that false webhooks could not be sent to our endpoint. As such, I was able to get a working subscription system, tested by myself as well as other interns through Stripe's test sandbox, and simulating many different events.

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

During one of my internships, our team was responsible for maintaining and diagnosing issues across a fleet of over 1,000 deployed camera devices. When a device experienced problems, like incorrect firmware versions or hardware issues, engineers had to manually SSH into each device to run diagnostic checks. This process was time-consuming and inconsistent, because each engineer might run slightly different commands or checks. It could take over two hours to fully troubleshoot a single device, and it became a bottleneck whenever multiple devices had issues at the same time. To improve this, I built a Python automation tool using Paramiko, which allowed us to remotely SSH into devices and automatically run a standardized set of diagnostic routines. The script performed checks like verifying firmware versions, running component diagnostics, and even triggering automated hardware actions like power cycling or fan control when necessary. By standardizing these checks and automating the workflow, we reduced troubleshooting time from about 2.5 hours to roughly 1.5 hours per device, saving the team about 10 hours of manual work each week. The biggest takeaway for me was realizing how much operational reliability improves when repetitive processes are automated, because it reduces both human error and the time needed to respond when systems fail.

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

During one of my internships, I was working on a backend system that processed documents using an LLM pipeline. Initially, the processing pipeline was fully synchronous, meaning each document had to be processed sequentially before the next request could begin. As more documents were added, this created a performance bottleneck, and processing a single request could take around 20 seconds. To address this, I redesigned the pipeline to use asynchronous task processing with Celery and Redis. Instead of handling the entire workload inside the API request, the system would enqueue jobs in Redis and allow Celery workers to process them asynchronously. This allowed the workload to be distributed across multiple worker processes, which enabled the system to process multiple documents at the same time rather than sequentially. By introducing this parallelization, we were able to reduce the end-to-end processing time from about 20 seconds to roughly 10 seconds during testing. The biggest takeaway for me was that performance issues often come from architectural bottlenecks rather than inefficient code, and introducing the right system design—like asynchronous workers—can significantly improve scalability.

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

When deploying one of my backend services on AWS using a serverless architecture, I realized that observability was critical to understanding how the system behaved in production. Serverless platforms like AWS Lambda scale automatically, which is powerful, but it also means performance issues can be difficult to diagnose if you don't have good monitoring in place. To address this, I designed observability dashboards using Prometheus, Grafana, and AWS CloudWatch metrics so we could monitor the system’s health and performance in real time. I focused on tracking several key metrics that would help us understand system behavior, including Lambda invocation counts, cold start frequency, memory utilization, and API latency. Monitoring these metrics helped us see how often new Lambda instances were being created, identify potential performance bottlenecks, and understand how the service behaved under different workloads. Having this visibility allowed the team to make more informed decisions about capacity planning and infrastructure tuning, instead of reacting only after issues occurred. This experience reinforced for me that reliability necessitates observability, to see what is going on and where.

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

While implementing a billing system using Stripe webhooks, I initially built the webhook handler to update user subscription states whenever an event was received. However, I didn’t initially account for the fact that Stripe may resend webhook events if it doesn’t receive a successful response. Because of that, the same event could be delivered multiple times, which meant the handler could potentially apply the same state update more than once. When reviewing logs during testing, I noticed duplicate webhook deliveries from Stripe retries, which revealed that the system could end up in an inconsistent state if the same event was processed multiple times. To fix this, I implemented idempotency checks in the webhook handler. I stored previously processed event IDs and verified whether an event had already been handled before applying any updates. This ensured that repeated events would not trigger duplicate state changes. This experience taught me an important lesson about distributed systems: when interacting with external services, you should always assume retries and duplicate events are normal behavior, not edge cases. Designing systems to handle those scenarios makes them much more reliable.

---

# Questions to Ask: Senior Site Reliability Engineer -> Manager

1. From my previous chat with Mr. Hartrich, I learned more about his work at FedRAMP High, which is what I am assuming I would be placed under. For your team specifically, do you collaborate with product or engineering teams, and if so, how? 

2. What kinds of reliability problems do new engineers usually underestimate when they first start working on large-scale systems?

3. What distinguishes interns who really succeed on your team?

4. What reliability challenges is your team currently focused on improving?

5. How does your team balance building new features with maintaining reliability?

6. What are some of the most important tools or systems your SRE team relies on day-to-day?
