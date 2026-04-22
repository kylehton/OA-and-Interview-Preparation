# Amazon Leadership Principles

---

***Below is a mapping of each STAR behavioral story to its umbrella of leadership principles.***

---

## Hardening Stripe Webhook Handler Against Duplicate Delivery

**Situation — Context:**

At ForOurLastNames, I owned the subscription billing pipeline — integrating Stripe's API and webhooks to keep user subscription state in sync with payment events. The core state model was small: a boolean `active` flag on the user and a `subscriptionID` field, updated on subscription create, update, and delete events.

**Situation — Trigger:**

I had what I thought was a working webhook configuration — signature verification via Stripe's header, user validation by ID cross-reference, event type and subscription state checks. Basic tests passed and the endpoints looked correct. Before shipping, I ran a longer mock sequence simulating real Stripe delivery behavior, including retries of identical events. In that run, I noticed the subscription start time was being rewritten on duplicate events and database writes were firing on every retry, even though the underlying subscription state hadn't changed.

**Action:**

- Investigated the retry behavior in Stripe's docs and confirmed webhooks are delivered at-least-once — duplicates and retries are expected, not exceptional.
- Mapped the handler's state space and recognized it was small enough that state-convergence checks could protect the core correctness property: `active` is a boolean, and "don't transition to a state you're already in" is a well-defined rule for every event type.
- Added state-validation guards at the top of each event type's handler — e.g., don't re-activate an already-active subscription, don't delete an inactive one, don't overwrite fields on a no-op update.
- Verified by replaying the full mock sequence with duplicate events and out-of-order retries, and confirmed no redundant state transitions.

**Result:**

Shipped the state-validation guards and cleared the last blocker on the billing pipeline. Replayed hundreds of duplicate events in staging with no corrupted subscription state. Pipeline went live for the investor beta on schedule.

**Learning:**

Two things. First, the technical one: at-least-once delivery is the default for any external webhook system, and passing basic tests isn't the same as being production-ready — duplicates, retries, and out-of-order delivery need to be designed for, not patched around. Second, the more general one: idempotent state transitions and idempotent *handlers* are different problems. State-validation protects the state field, which was the correctness property I needed. But if the handler ever grew side effects that weren't state-gated — emails, analytics writes, downstream API calls — state checks wouldn't protect those. The stricter solution is event-ID deduplication at the handler entry point, and that's the approach I'd reach for now if I were building a webhook handler with richer side effects.

**Follow-Up:**

*Why state validation instead of event-ID deduplication?* 

The state space was small and the correctness property was narrow: keep the `active` boolean and `subscriptionID` consistent under duplicate delivery. State validation on a boolean is naturally idempotent — setting `active = false` twice produces the same result as setting it once, and explicit state checks prevent nonsensical transitions. For the scope of what the handler actually did, it was sufficient. The stricter implementation would be an event-ID dedup store with a TTL covering Stripe's retry window, checked at the top of the handler before any processing. That approach generalizes better because it protects arbitrary side effects, not just state transitions — which is exactly why I'd use it if the handler's scope grew. At the time, for a boolean flag and a string field, state validation was the right tradeoff between correctness and implementation cost.

### Leadership Principles

**1. Dive Deep:** Emphasize running the longer mock sequence as a final check after basic tests passed, tracing the duplicate writes to Stripe's at-least-once delivery semantics, and understanding the problem deeply enough to know both what was sufficient for this handler and what the stricter solution would look like.

**2. Insist on the Highest Standards:** Emphasize holding the bar above "basic tests pass" — running adversarial replay scenarios before considering the pipeline production-ready.

**3. Learn and Be Curious:** Emphasize the reflection in the Learning section — shipped a fix that was correct for the scope, then came to understand its limits and what the next iteration would look like. The "what would you do differently" answer is already built in.

**4. Ownership:** Emphasize responsibility for billing correctness before release — catching and fixing the duplicate-write bug as the owner of the pipeline, rather than shipping and hoping.

---

## Taking Action to Fill a Gap

**Situation — Context:**

I was the backend engineer on a 4-person engineering team, frontend, data, AI, and me, building an internal LLM-powered resume tool at PM Accelerator. About halfway through, our data engineer had a family emergency and dropped out completely.

**Situation — Trigger:**

In the first half of my internship, I built the server side with FastAPI, working on integrating with the React frontend UI. We needed a persisted database and schema to store user data and resumes — for improvement, conversion, and download — and the data engineer who owned that work was no longer present. Without it, the FastAPI backend I'd been building had nowhere to read from or write to, and the AI intern's pipeline had no inputs.

**Action:**

- Assessed the gap within a day — what the data engineer had committed to, what was missing, what downstream work was blocked, such as resume storage, retrieval for analysis, download.
- Made the call to absorb the role rather than escalate for a replacement, since timeline didn't allow for onboarding a new person.
- Negotiated coverage with the frontend intern, handed off the React-side endpoint integration I'd been doing so I could focus on database work without dropping my own commitments.
- Taught myself MongoDB from scratch and designed the schema for user documents and resume storage, prioritizing the fields the AI intern's pipeline needed as inputs.
- Coordinated with the AI intern in short daily syncs to keep model inputs aligned with the new schema as it took shape.

**Result:**

Shipped the database and schema in time to integrate with both the FastAPI backend and the AI intern's LLM pipeline. MVP demoed on schedule to the mentor and CEO with no reduction in scope, despite losing 25% of the engineering team mid-project.

**Learning:**

I learned the importance of taking action and collaborating with others. I now know that "absorb someone else's work" only works if you actively redistribute your own work first, otherwise you overload your own workload and ending up pushing back or missing deadlines. Collaborating directly with the frontend intern to distribute the tasks to complete was the vital move that made shipping the MVP on time a reality. Additionally, through my direct work, I learned how to configure the basics of MongoDB, and implement that within an application.

**Follow-Up:**

*What would you do differently?*

I would have reviewed the schema design with someone before committing to it. I built what worked for the MVP demo, but I was making decisions about document structure and field organization without any review, and in hindsight, some of those choices wouldn't have been optimal if the system scaled. Even asking the AI intern to spend 20 minutes reviewing the schema before I built against it might have caught things I didn't know to look for.

### Leadership Principles

**1. Bias for Action:** Stepping up to take action in a moment of vagueness and lack of clarity upon disappearance of the data engineer intern.

**2. Ownership:** Owning the entirety of the project together, acting and working on behalf of the team, not just of my role.

**3. Earn Trust:** Gained and utilized the trust of my team, specifically from the frontend intern, to work cohesively towards building the application while bridging the database implementation gap.

---

## 0 to 1 Planning and Execution

**Situation — Context:**

ForOurLastNames is an early-stage financial education platform. As we approached beta release, I was tasked with standing up production hosting on AWS for a small investor-trial user base — pre-revenue, with explicit pressure to minimize cloud spend since every dollar of runway mattered

**Situation — Trigger:**

I was given no technical spec, no architectural preferences, and no engineer senior to me on the project — just a directive to get it deployed and keep costs low. The only constraints came from the CEO and CTO's business context, not from engineering. I had to define the problem, research options, and own the recommendation.

**Action:**

- Researched different AWS server deployment options, like Lambda and EC2, as well as compiled all findings into presentations and spreadsheets
- Presented at multiple stand up meetings with the CEO and CTO, to align on expectations as well as explore options that aligned with their thought processes
- Given the nature of the front-end application being a Vite static page application, I chose CloudFront + S3 to host. Static asset hosting from S3 is effectively free at low traffic and CloudFront gives us CDN-level performance without a dedicated server.
- Chose API Gateway + Lambda (container-deployed Express server) over EC2 because the investor-trial traffic pattern was low-volume and bursty, Lambda's scale-to-zero meant we'd pay nothing during no-usage windows, which EC2 couldn't do.
- Deployed and migrated all PostgreSQL table schema to Supabase, enforcing Row Level Security policies per-user
- Went above and beyond in building an observability layer using Grafana, Prometheus, and CloudWatch Exporter, tracking CPU and memory utilization per Lambda function, which would let us make informed resource-allocation decisions and would give us baseline data if we ever needed to migrate off Lambda as traffic grew.

**Result:**

I shipped the full-stack deployment for the investor beta on schedule, with total monthly cloud spend under $30 fully loaded — Supabase at ~$10/month plus AWS costs for Lambda, API Gateway, S3, and CloudFront. The scale-to-zero Lambda architecture was the main cost driver: during idle windows, which was most of the time for an investor trial, we paid effectively nothing for compute. Separately, I built out a local observability stack using Grafana, Prometheus, and CloudWatch Exporter — validated against test data but intentionally not deployed to production, since the investor-trial volume didn't justify the cost and the goal was to have the tooling ready to stand up when traffic patterns warranted it. The deployment supported the full investor trial without incidents.

**Learning:**

I learned that cloud architecture is a series of tradeoffs against the actual traffic profile, not a set of best-practice defaults. The instinct as a junior engineer is to reach for what you've seen elsewhere — EC2 because it's the "standard" option, RDS because it's the AWS-native database — but those choices only make sense if your workload matches their strengths. Our workload was low-volume, bursty, investor-trial traffic with tight cost constraints, so scale-to-zero Lambda over always-on EC2 and Supabase over RDS were the right calls for this situation, even though they wouldn't be for a high-throughput production service. I came out of this with a clearer mental model of matching architecture to workload rather than picking based on familiarity.

I also learned that if possible, you should build the tooling before you need it, but don't turn it on until you do. I put the observability stack together locally and validated it worked, but kept it off production during the trial because the traffic didn't justify the cost. If we'd needed to debug a production issue or if traffic patterns had shifted, we wouldn't have been starting from zero — we'd have had the stack ready to deploy. Retrofitting observability under pressure is always more expensive than building it in advance and leaving the switch off until it's needed.

**Follow-Up:** 

*Why build it at all if you weren't going to run it?*

The observability dashboard was to prepare for future full launch in its very first stage, and watch the deployment until it would be more cost-effective to scale up to EC2. Given the configuration of S3 and CloudFront, as well as Supabase being scalable and production ready, I only really needed to worry about the computational cost of Lambda functions spinning up per function call. This would only really be an issue once usage started getting high, reaching limits in resource allocation. Increasing resources at a specific scale for Lambda functions is more costly than an always-on EC2 instance with the same computational power, which is the point of conversion that would be shown in the dashboard upon getting close to or reaching consistent high usages.

### Leadership Principles

**1. Dive Deep:** Researched heavily on different deployment options, compiling a thorough analysis of each option, with constraints in mind

**2. Frugality:** Focused selection in deployment tools around minimizing deployment costs given the early-stage of the company with little current funding

**3. Deliver Results:** Delivered checkpoint presentations to communicate current standing with CEO and CTO, converging to the most optimal selection and executing the full deployment, resulting in the full user-ready beta application being deployed onto the cloud

---

## Efficiency Improvements through Asynchronous Task Queues

**Situation - Context:**

The PM Accelerator internal resume enhancement tool was built to help product management interns improve their resumes using an LLM pipeline, parsing resume sections, injecting role-relevant keywords, and rewriting bullets for stronger impact. I owned the backend and was testing the end-to-end workflow ahead of internal rollout.

**Situation - Trigger:**

I noticed that for longer revisions across the entire resume, the time taken for the computation and LLM API calls were taking an extremely long time, averaging around 20 seconds in total. Nobody had flagged this as a blocker, since basic tests passed and the tool worked. But 20 seconds of wait time on a single button click is high-latency, and would definitely make users assume something was broken and abandon it altogether, and I didn't want to ship that type of bar even for an internal tool.

**Task:**

I wanted to essentially find a way to speed up the entire process, so the user would not have to wait so long for a full resume keyword enhancement operation.

**Action:**

- Analyzed the bottleneck and confirmed the 20-second average was driven by sequential LLM calls across resume sections (Experience, Projects, Education, Skills) — each section blocked on the previous one finishing, despite having no actual interdependencies.
- Created a message queue using Redis to store incoming tasks.
- Configured multiple Celery workers to execute tasks concurrently, pulling from the async task queue.
- Considered FastAPI's built-in BackgroundTasks as a lighter-weight alternative, but decided against it: BackgroundTasks runs in the same process as the request handler, which means tasks die if the server restarts mid-execution and there's no built-in retry or visibility into task state. For LLM calls averaging several seconds each — with real failure modes like rate limits that would benefit from retry — the durability and observability of a dedicated broker-backed queue (Celery + Redis) was worth the extra setup cost.

**Result:**

I optimized the task execution workflow to ensure it was leading to more efficient function calls and resume processes. Over informal testing, we measured that this implementation resulted in a 50% decrease in the duration of the entire flow (from 20 seconds to 10 seconds), where it was bottlenecked by the longest individual enhancement, generally in the Experience section.

**Learning:**

Something working and something being ready to ship to users are different bars, and the gap between them is where the user experience varies. Twenty seconds wasn't a bug since the tool worked correctly, and for an internal tool with no external users, many engineers would have stopped at that. However, the user experience was not at a high standard, and that was something I did not want to ship. Taking the time to refactor and approach things from a different angle to optimize the product for users is the main focus I took away from this entire experience.

**Follow-up:**

### Leadership Principles

**1. Insist on the Highest Standards:** Through upholding a high standard, I was able to implement an async task queue that resulted in an extremely significant decrease in wait-time for processing. This directly improved user experience in employees and interns improving their own resumes using our tool.

**2. Dive Deep:** To pinpoint the bottleneck in the end-to-end function flow, I dove deep into analyzing the entire call, function by function. Through that, I was able to discern the issue and directly address that.

---

## Conflict and Compromise

**Situation - Context:**

Nearing the end of my internship, I was asked to join the intern leading a new functionality in storing historical credit score data per user for a later implementation of showing change over time. We essentially had to plan out the stack used as well as an actionable list of executable tasks for the next interns. The two of us decided to do research on how we would model the stored data, and the best way to approach this new addition into the current application.

**Situation - Trigger:**

We ended up selecting different databases to store this. I decided to stick with the current PostgreSQL implementation, while he wanted to utilize MongoDB.

**Task:**

I had to find a way to sync up with him and come to a compromise, to unblock our path and work together towards drafting a plan to implement this.

**Action:**

- Clarified the schema design first, I realized part of his initial space-optimization concern assumed I was proposing credit score rows in the main users table, which would have scaled poorly. My actual proposal was a separate history table joined by user ID, which only grows when real scores are reported. Once that was clear, his space objection resolved.
- He pivoted to query performance: retrieving a full history for one user from a single Mongo document would be faster than a Postgres lookup joining two tables.
- I conceded the partial validity of that argument, since a single document fetch could be marginally faster than an indexed foreign-key query, but argued the overall tradeoff didn't favor Mongo. The marginal performance gain was on a single access pattern; the cost was adding a second database to our stack.
- He was sizing the decision for the investor demo, where Mongo's free tier would cover the cost. But the moment the feature scaled past the free tier or we needed to migrate for any reason, migrating document-structured credit score data into a relational schema would be meaningfully more work than just starting relational. We'd be creating migration debt to save a small amount of short-term infrastructure cost.
- He acknowledged the assumption he'd been operating on, that he'd been sizing the decision for the investor demo specifically, and agreed the forward-looking tradeoff favored Postgres.

**Result:**

We aligned on the Postgres + separate history table design and drafted the implementation plan together. The following cohort shipped the feature using that design. The decision also kept the stack simpler for subsequent interns — one database to learn and operate instead of two, which was a secondary benefit neither of us had initially weighed.

**Learning:**

I learned that in making technical decisions, there are almost always a variety of factors to consider. We ended up going through multiple different points of discussion before compromising and selecting a path to follow. 


**Follow-up:**

### Leadership Principles

**1. Have Backbone, Disagree and Commit:** Held a technical position under peer disagreement with someone who had formal lead authority on the feature and made my case based on forward-looking tradeoffs rather than winning on the narrower axis being argued. We both conceded the partial validity of the opposing arguments, coming to a resolution based off the best implementation for minimal technical debt and operation cost.

**2. Frugality:** The decisive argument was about operational cost and migration debt, avoiding a second database instance when an existing one could handle the workload cleanly, and specifically avoiding the forward-looking cost of migrating document data into relational form. 

**3. Are Right, A Lot:** The technical judgment held up, the Postgres and separate history table design was shipped by the next cohort and worked as intended. The judgment that migration debt outweighs short-term infrastructure savings is the kind of tradeoff call that's easy to get wrong as a junior engineer, and the call was correct.

---

## Automating a Manual QA Workflow Nobody Asked Me To Fix

**Situation — Context:**

During my internship at Trace, I worked with the Quality Assurance team on camera firmware testing. The QA engineers ran scripts to test camera software and hardware across multiple device versions, and the results, along with the specific versions tested, had to be logged into Google Sheets for bi-weekly auditing.

**Situation — Trigger:**

I noticed the version-logging part of the workflow was still manual. For every test run, engineers were opening virtual machines, checking the camera firmware version, writing it into the spreadsheet alongside the test metrics, and doing this repeatedly across test cycles. It added meaningful downtime to what should have been an automated pipeline, especially during bi-weekly audits where version accuracy mattered most. Nobody had flagged this as a problem, it was just how things had always worked, but watching the engineers do it made it clear that their time was being spent on mechanical bookkeeping rather than actual test design and analysis.

**Action:**

- Observed the existing workflow across a few test cycles to understand what the engineers were actually doing manually, not just the version lookup, but how the versions mapped to the test metrics they were logging alongside.
- Identified the integration points: the testing scripts already had access to the VMs and were pulling test metrics programmatically, so the version information was already reachable in code, it just wasn't being captured.
- Extended the existing testing scripts to parse camera firmware version alongside test metrics during the test run itself, using Python and Paramiko SSH.
- Integrated with the Google Sheets via PyGSheets, logging directly so versions and metrics were written together into the audit spreadsheet, eliminating the manual lookup and entry step entirely.
- Validated against a full test cycle to confirm the versions being logged matched what engineers would have entered manually.

**Result:**

Eliminated the manual version-lookup-and-entry step from the QA workflow. Engineers got that time back for actual test design and triage work, and the bi-weekly audits became more reliable because version-metric pairings couldn't drift out of sync (they were now written together in one pass, rather than looked up separately). 

**Learning:**

The biggest thing I took from this: "that's just how we do it" is often a flag that a process hasn't been questioned, not that it's optimal. The engineers weren't complaining about the manual version logging because they'd accepted it as part of the job, but watching their workflow from outside made it obvious it shouldn't have been their job at all. Small, unglamorous automation that removes friction from someone else's day can have outsized impact, and looking for those opportunities — especially as the newest person on a team, with fresh eyes on the workflow — is a habit I've carried forward. The narrower lesson: when the data you need is already flowing through a system, capturing it at the source is almost always cheaper than reconstructing it later.

**Follow-Up:**

*Why didn't the QA engineers automate this themselves?*

It wasn't anyone's explicit responsibility to improve the tooling, the QA team was focused on test coverage, and script maintenance was a side concern. I had time outside of my standard tasks, so it made sense for me to take it.

*How did you know this was the right thing to spend your time on?* 

I had slack in my workload, I'd observed the workflow enough to know the pain was real, and the change was low-risk (extending an existing script, not introducing new infrastructure). The downside if it didn't work was small; the upside was freeing up recurring engineer time.

*What would you do differently?* 

I'd have checked in with the QA lead before shipping, not to ask permission but to make sure I understood any constraints on the audit process I might have missed. It worked out fine, but deploying a change to someone else's workflow without a quick double-check conversation was a small gap in my approach.

### Leadership Principles

**1. Customer Obsession:** My customers were the QA engineers. I observed their workflow, identified friction they'd stopped noticing, and removed it, without being asked and without them having to advocate for the fix. The change was small, but it was built entirely around reducing their pain points, not around producing something flashy for my own resume.

**2. Ownership:** Took responsibility for improving a process that wasn't in my job description, because I had the skills and the bandwidth and the work mattered to people on the team. Ownership at Amazon is specifically about acting beyond your stated role when the team needs it, and this was a clean case of that.

**3. Bias for Action:** Moved from "I noticed a problem" to "I shipped a fix" without a lot of process overhead. The change was low-risk enough that asking for permission would have been higher-friction than just building it, validating it, and handing it off.

---

## Teaching Myself Production ML Patterns Through Labl

**Situation — Context:**

Labl is a personal project I've been building, an AI-powered email labeling system that learns a user's labeling patterns over time and auto-classifies incoming mail. The architecture combines BAAI/bge-small-en-v1.5 embeddings with BM25 sparse search for hybrid retrieval, a medoid-bootstrapped classifier that graduates to k-means clustering as confirmed labels accumulate, Celery + Redis for async processing, MongoDB for label history, and FastAPI for the backend. I started it because I had always wanted some sort of tool to help manage my inbox. After using Notion Mail's AI labelling feature, I felt as though it was not as accurate as I wanted it to be. So, I decided to try and built it myself.

**Situation — Trigger:**

Most ML tutorials stop at "fit a model on labeled data and make predictions." The problem I actually wanted to solve didn't fit that shape. I had essentially zero labeled data on day one for any given user, the system had to work with a single confirmed label and get better as more labels accumulated. That meant I couldn't just reach for scikit-learn's default clustering and call it done; the clustering algorithm itself needed to behave differently depending on how much data I had. I didn't know how to design that, which meant the project became a sequence of "I don't know what the right answer is here, let me figure it out" decisions rather than executing a known recipe.

**Action:**

- Evaluated embedding models before committing to one. Compared BAAI/bge-small-en-v1.5 against all-MiniLM-L6-v2 on retrieval accuracy vs. latency for the email-content use case. Chose BGE-small because the accuracy gap was meaningful enough to justify the slightly higher latency. Considered BGE-base as a future upgrade path but left it as a deferred decision pending real-world usage data.
- Designed classification system to work from a small subset of confirmed labels, and build on each iteration, becoming more accurate in relation to the growing confirmed labels from a user's inbox.
- Layered BM25 sparse search rather than relying on semantic similarity alone. Emails frequently contain lexical signals (sender, subject keywords, specific terms) that pure embedding search underweights.
- Built skip-on-conflict write guards to prevent destructive writes to live user inboxes. Since the system operates on real email data, any bug that incorrectly modified or deleted emails would be actively harmful — not just a correctness problem. Treated this as a design constraint rather than a late-stage concern.
- Chose privacy-conscious model and deployment decisions: ran embeddings locally rather than sending email content to hosted LLM APIs, designed the schema to avoid persisting email content beyond what was needed for labeling, and treated user email data as high-sensitivity by default.

**Result:**

The system works end-to-end: new emails get embedded, retrieved against historical labeled data via hybrid search, classified by the adaptive classifier, and surfaced for user confirmation before any labels are applied. More importantly, I have a far better understanding of embedding models, retrieval architectures, clustering algorithms, and async job systems, and am actively working on configuring full production level operations to someday release to the general public.

**Learning:**

The biggest lesson wasn't technical: it was learning that privacy and data constraints aren't late-stage concerns to bolt on, they are design constraints that should shape the architecture from the start. My first pass at the project was centered on using hosted LLMs like GPT or Claude for the classification logic. When I looked into it more, I realized those APIs retain queries for future training, which meant sensitive email content would be stored on third-party infrastructure, which was a privacy problem I couldn't engineer around. I considered hosting a local LLM instead, but that introduced a different problem: lower base accuracy, and without a broader training dataset than my own inbox, any custom fine-tuning would just encode my own labeling bias into the classifier. Each option had a disqualifying failure mode I didn't see until I actually looked at it. The right move wasn't to force one of those options to work, it was to step back and ask whether the project needed a generative LLM at all, which led me to the embedding-plus-classical-ML approach I ended up with. This was the first time I really had to consider user-data privacy in more than one part of the code base. Building this project taught me to place user privacy, data sovereignty, and bias at the forefront of design on any system that handles user data, not as compliance checkboxes to add at the end.

**Follow-Up:**

*Why not just use an off-the-shelf LLM API for classification?* 

Two reasons. One: privacy. Sending email content to a hosted LLM API creates a data exposure surface I wasn't comfortable with for a tool operating on real inboxes. Two: local inference with a specialized embedding model is cheaper at scale than paying per-token for every classification — the tradeoff tilts further toward local as usage grows.

*Why medoid-to-k-means instead of just starting with k-means?* 

K-means is unstable at very low sample counts — with 2-3 confirmed labels, you'd get cluster assignments that shifted dramatically with each new data point. Bootstrapping from a medoid gives a stable anchor point for early classification, and graduating to k-means once there's enough data to form real clusters. The threshold (~30 confirmed labels, K=5) was a tuning decision based on observed behavior, not a theoretical result.

*Why both dense embeddings and BM25?*
  
Dense embeddings capture semantic similarity but underweight specific lexical signals (a specific sender, a specific keyword) that matter a lot for email classification. BM25 captures those lexical signals directly. Running both and combining the retrieval results caught failure modes that either alone would have missed.

*What's still unfinished?* 
Honest answer: ML feedback loop validation, the async job system, label history/undo, review queue UI, and EC2 deployment. The core classification and retrieval pipeline works; the production-readiness pieces are still in progress.

*What would you do differently?* 

I'd have started with a smaller scope and shipped sooner. The project has become ambitious enough that getting to full deployment has taken longer than if I'd cut features. "Working end-to-end on my own inbox" would have been a viable v1; I'm essentially building v2 before v1 shipped.

### Leadership Principles

**1. Learn and Be Curious:** The entire project is an exercise in going past the tutorial-default answer at every design decision. Embedding model selection, clustering approach at low-data, hybrid retrieval, write safety, and each one was a case of recognizing I didn't know the right answer and investing time to understand the tradeoffs before committing.

**2. Dive Deep:** The medoid-to-k-means graduation design is the clearest example, recognizing that off-the-shelf k-means would fail silently at low sample counts required understanding the algorithm's behavior deeply enough to design around its failure mode. Most personal ML projects wouldn't have caught this.

**3. Are Right, A Lot:** The specific architectural choices, like BGE-small over MiniLM, hybrid retrieval over dense-only, and local inference over hosted APIs were judgment calls made with limited information, and each one has held up under real usage. None are the obvious default, and each has a defensible case.

---

## Building Git Lint: An Event-Driven AI Code Reviewer

**Situation — Context:**

Git Lint is a personal project I built around 11 months ago: an automated AI-powered code reviewer that runs on every pull request to my GitHub repositories. The system is event-driven, conditioned on GitHub's pull request webhook, and does three things: pulls the diff from the PR, contextualizes the changes using RAG against a vector database of the repository's prior code, and posts a structured summary of changes, improvements, and issues as a comment on the PR.

**Situation — Trigger:**

I wanted a code reviewer for my own projects, something that would give me another pair of eyes on PRs before I merged them, especially on solo work where no human reviewer was available. Additionally, I'd never worked with Pinecone or vector databases, had barely used S3, and wanted a concrete reason to learn both rather than going through a tutorial and forgetting everything a week later. The project was as much a learning opportunity as it was a tool to be used.

**Action:**

- Designed the architecture before writing code: event-driven via GitHub webhooks, vector database (Pinecone) for storing embedded representations of repository code, S3 for storing larger artifacts and diffs, and an LLM call in the middle to synthesize the review comment. Each component was a technology I hadn't used in production before.
- Learned Pinecone from scratch: index configuration, embedding schema, upsert patterns, query patterns, and the tradeoffs between index types for the repository-scale data I was dealing with. Made decisions about dimension size and metadata filtering based on the access patterns I expected.
- Configured S3 for the auxiliary storage, mostly learning IAM permissions, bucket policies, and the specific patterns for integrating S3 with a Lambda-based event handler.
- Designed the self-sustaining feedback loop: each PR analysis not only generates the review comment but also updates the vector database with the new code, so the tool's context keeps current with the repository automatically. This was the design choice that made the system "build-and-forget" — there's no manual retraining or re-indexing step because ingestion happens as a side effect of review.
- Tested the webhook pipeline end-to-end by testing against my own repositories, mocking changes in code that would cause error, and testing catch rates. Iterated on the LLM prompt until the reviews were consistently useful rather than generic.

**Result:**

The tool has been running for roughly 10 months across my personal repositories without intervention. I've never had to fix a bug in it or manually update the vector database. Every PR I open on a Git Lint-enabled repo gets a context-aware review comment within a 10 seconds of opening. The tool has actually caught issues in my own code that I missed, inconsistent error handling, missing edge case coverage, style drift from prior code in the same module, which is the specific validation that the RAG context is working as intended and not just producing generic LLM output.

**Learning:**

Two lessons, one technical and one about project design. Technical: vector databases and retrieval-augmented generation look complicated from the outside but come down to a few core design decisions: embedding model choice, index structure, query patterns, and how you handle updates. Once I'd worked through those decisions once for Git Lint, the next RAG project (Labl) was much faster to stand up because I understood the underlying pattern, not just one specific implementation.

Project design: the "build-and-forget" property didn't happen by accident. It came from the self-updating feedback loop and from spending extra time upfront on the webhook-to-processing flow so there were no manual intervention points. Designing this to be self-sufficient turned out to be a good forcing function for thinking about reliability and maintenance.

**Follow-Up:**

*How does the self-updating loop work without causing infinite loops or polluting the vector DB with bad code?*
  
Updates only happen on PRs that are just opened, not accepted ones, so the vector DB only ingests code that the has not been merged. The feedback is then reviewed by an actual human, along with an actual code review to reaffirm the summary analysis.
  
*How do you know the RAG context is actually helping vs. the LLM just producing plausible-sounding reviews?*

Through testing, I read the comments, especially where they referenced older parts of the codebase that integrated with the new changes within the diff. I validated the analysis in those parts, ensuring that the RAG was giving context that actually helped towards a more holistic analysis.

*What would you do differently?*

I'd have set up some form of lightweight evaluation, even just a manually curated set of "good review" vs. "bad review" examples, to have a way to validate prompt or model changes without relying on spot-checking. A lot of the iteration was done by polling the same webhook repeatedly, and comparing each change to the prompt with its corresponding response.

### Leadership Principles

**1. Learn and Be Curious:** The project was explicitly a learning vehicle for technologies I hadn't used — Pinecone, vector databases, RAG patterns, S3 configuration, GitHub webhook integration. I picked a concrete problem that required learning all of them together rather than doing isolated tutorials, because understanding how the pieces fit was the real skill I wanted to build.

**2. Ownership:** I built a tool I knew I'd be the sole maintainer of, and I designed it to minimize the maintenance burden on my future self. Ten months of uninterrupted operation isn't luck — it's evidence that the self-updating feedback loop, the webhook-based event architecture, and the testing I did at build time paid off. Designing for long-horizon reliability as the only person who'd feel the cost of failure is a form of Ownership that generalizes to production work.

**3. Invent and Simplify:** The self-updating feedback loop is the core simplification — by making ingestion a side effect of the existing review pipeline, I eliminated the "keep the vector DB in sync with the repo" maintenance burden that a naïve design would have. The alternative architectures I considered all had explicit sync steps that would have needed to be monitored and occasionally repaired. Removing that entire category of failure mode was the key design win.

---

## Task

**Situation - Context:**

**Situation - Trigger:**

**Task:**

**Action:**

**Result:**

**Follow-up:**

### Leadership Principles