# Resume-Specific Questions Leaning towards Mechanize

Drafted questions that I think Mechanize would ask considering their domain in RL learning for LLMs, and pointed questions during intro screening. Questions primarily focused around Git-Lint, Labl, where they asked about LLM integration, feedback loop, evaluation in LLM response, use cases.

---

## Background / Fit

1. Tell me about yourself.

>I'm Kyle, a rising senior at UCSD studying Math and Computer Science, hoping to get into software engineering specifically in AI integration and security. I have interned at a few different places in the past, most recently at AWS. My professional experience spans across backend development, cloud service hosting and deployment, as well as building end-to-end features and systems. In my initial internship at Trace, I did quality assurance testing, essentially writing scripts to build on the current troubleshooting and testing practices. Following that, I did backend server development using FastAPI for an internal tool using a custom-trained LLM for resume improvements. I then interned at ForOurLastNames, where I worked on deploying the company application onto AWS, as well as implementing payment and billing through Stripe. Currently, I am interning at AWS building a triage agent event-driven pipeline to assist in triaging security and compliance issues.

2. Walk me through your background and the experiences most relevant to Mechanize.

>I would say the experiences most relevant to Mechanize would be my two listed projects. Starting with projects, I have worked with feedback loops through my project, Labl. For context, Labl is a classification system project, designed to automatically classify emails to pre-set and custom created labels using embedding centroids and similarity search, more traditional machine learning. The part that is most relevant to Mechanize through that would be the feedback loop. Essentially, for confirmed labels by the user, the stored centroids for a given label are recomputed so that each iteration creates a centroid closer and closer to the type of categorically correct email in the user's inbox, hopefully providing personalization to the system. Additionally, with a certain threshold of confirmed samples, the system graduates to a k-means clustering system, allowing for more accurate representations of pre-set and custom labels. As for my other project, Git-Lint, that project was meant as a code improvement tool when I first started building on my own. It analyzes diffs and pulls context using RAG in order to view code changes and determine their quality as well as recommended changes to fix issues or follow convention. There is no formal evaluation step for that, as it was a quick spin-up tool for me to improve my own code quality. I would take into account the responses I got back, iterate on the prompt, until I was consistently receiving comments that helped me improve my code quality.

3. Why Mechanize?

> I am interested in Mechanize because I think that it serves to address a real bottleneck in current LLM performance. It is well known that long-horizon tasks tend to stretch the context window, causing the LLM to potentially hallucinate and deteriorate in overall quality. The quality of response is extremely important in this day and age not only because it is used in production systems across software, but also because of the nature of AI. As more and more responses are generated through AI, they increasingly take up a portion of the world's current generation of data, which will be used in the future to train LLMs and AI models as well. Maintaining low quality results leading to low quality data will only make it easier for the current progression of AI to plateau.

4. Why are you interested in AI agents and reinforcement learning?

> I am interested in AI agents and reinforcement learning for agents because I think agentic workflows and integrations are undoubtedly the path into the future. This is already something that is common in the tech sector, with agentic integrations in software engineering, entire startups dedicated to agentic approaches to productivity and assistance (for example, Dex), and as AI becomes more capable, this is only going to expand. I want to become as AI-native as I can, because I think these integrations are a force multiplier for what an individual can do. I am also a big proponent of learning and growing, and I use LLMs heavily for that, as a tutor and such. Increasing the quality and accuracy of LLMs and AI models only allows for increased learning capabilities for this use case, which would be amazing

5. Which project or internship experience best represents your technical ability?

> I think my current internship at AWS best represents my current technical ability. Although the agentic aspect is not as developed in my project, I have covered many parts of the codebase that my project is native to, as well as other applications and codebases in my team. I have made numerous changes that have made it to production at AWS, and these are things that few interns experience and do. I think the technical ability that is demonstrated best here is my ability to quickly onboard and involve myself. Through learning and practice I have been able to actively participate in architectural and design discussions with my mentor, manager, and principal architect, in which no other intern in our organization has done.

6. What is the hardest technical problem you have solved?

> The hardest technical problem I have solved has been designing the event-driven pipeline in my current internship. There were many different requirements between my manager and architect, and my project wasn't fully finalized even 4 weeks into my internship. With that said, I navigated the uncertainty and ambiguity and went through several iterations of my pipeline, gathering feedback from the necessary sources and finalized my design.

7. Tell me about a technical decision you would make differently today.

> One decision I would have made differently today would have been reinforcing the idempotency check for my Stripe implementation in my internship at ForOurLastNames. The idempotency check was done through status checks, only applying subscription changes on valid statuses and such, which kept behavior predictable for webhooks. However, I think having an explicit deduplication step would have reinforced idempotency and made the system much more defensible. If I could do it over and had a little more time, I think this is what I would have liked to see in my final finished implementation.

---

## AWS Bedrock Agent

1. Tell me about the Bedrock triage agent you are building at AWS.

> The triage agent I am building at AWS, to be completely transparent, is an exaggeration of an agent. Currently it is in an infantile stage, where it is an agent provided with a few tools to determine a control mapping and root cause for a given issue. These tools are a KB query, as well as an LLM-rooted classification prompt with the categories and descriptions as context. It is not truly advanced as an agent, but the decision made by my manager and architect were as an initial phase implementation. In the future, they envision the expansion of the agent's capabilities in the triage process, extending into actively helping resolvers remediate the issue.

2. What makes that system an agent rather than a normal LLM pipeline?

> Right now, the agent technically can be replaced with an LLM pipeline given the simplicity of tooling and purpose behind the agent. However, the agentic process behind it is that it determines which tools to call and how it completes the intended output. As of now, there are a very limited set of tools at its disposal which makes it pretty deterministic as to which tools it will call.

3. How does the agent decide when and which tools to call?

> The agent is given the tooling with appropiate descriptions in their functionality, input, and output, so it gains an understanding of all the tools at its disposal. Right now, there is an explicit check regarding the output data model to ensure they are all filled, and the agent is reprompted to ensure the output is completed using its own reasoning and the tools at its disposal when necessary.

4. How do you determine whether the agent’s output is correct?

> The nuance here is that a different organization is the user demographic for this agent, which is the organization that actually remediates and resolves these issues. Given the primitivity of this implementation, the agent, before release, must meet specific accuracy metrics against a human-confirmed issue set and match the control mapping and root cause classifications. The agent output itself is used as additional help and not a source of truth, so any wrong information is at the prerogative of the resolver group for the issue.

5. What happens when the agent has low confidence?

> The agent flags the specific generated insight for human review, and so the resolver group user knows that the overall quality of the response may not be accurate.

6. What are the main failure modes you have seen or would expect from this agent?

> The agent is fairly new and not yet in production, so no explicit failures have been seen. The only current discrepancy is the reusing of a knowledge base within my team, which is not fully accurate because of a lack of maintenance.

7. If you had to build an evaluation suite for this agent, what would you measure?

> If I had to build an evaluation suite for the agent, I would measure the tools called, to ensure tool calling coveres the entire breadth of the task given to the agent. I would then look at reasoning and state correctness, to see how it interpreted the result from tools, whether it progresses in different stages of its task without wasting additional tool calls or tokens, and contextual grounding if possible.

8. How would you prevent the agent from getting a high score for the wrong reasons?

> With the way the current environment for remediation and control mapping is, it would honestly be difficult to prevent the agent from getting an extremely high score or low score. My task involved implementing a tool out of my control, which already abstracts any improvements and accuracy tuning I can do. With that said, there is no set of information that I can use for root cause classifications that is not extremely redacted or confidential.
---

## Mechanize / RL / Agent Evaluation

1. What do you understand about what Mechanize does?

> From my understanding, Mechanize is a reinforcement learning system creation startup, focusing on improving LLM performance for long-horizon and heavy reasoning tasks. The main goal of Mechanize is to consistently create tasks for an LLM/agent to attempt that approaches its computational and reasoning limits. In doing so, it validates model output, agentic thought processes, in a way that provides direct and detailed feedback for points of improvement. I think the difficult scope of this is creating the actual test suite to evaluate agent output for these tasks. This requires mastery over the creation of the task and all components associated with the task and its subtasks.

2. What would an RL environment for a coding agent look like?

> An RL environment for a coding agent would ideally be as follows: the agent would be given an explicit task with detailed descriptions, and a few different things would be evaluated. The first would be reasoning. Depending on the level of autonomy given to the agent for the planning, the reasoning behind architectural decisions and action items would need to be evaluated to ensure that the agent considers different approaches, performance and security concerns, and other system design type topics. As for its output, it would need to be evaluated for its intended use case as well as edge cases. Something that AI generated code misses out on often is covering edge cases, as it builds the code modeled off of the intended use case and behavior. Code concision and quality is also something that should be evaluated, to ensure that there is no redundant code, redundant logic, and dead/useless parts of an implementation.

3. In that environment, what would the state, actions, reward, and episode be?

4. What makes a good coding-agent evaluation?

5. What is the difference between evaluating an LLM and evaluating an agent?

6. What is reward hacking? Give an example involving a coding agent.

7. What makes a good reward signal for a long-horizon software-engineering task?

8. How would you tell whether a coding agent actually solved a task versus overfit or gamed the grader?

9. What do you think are the biggest current limitations of coding agents?

---

## Labl / ML

1. Walk me through Labl’s classification pipeline.

> An email comes in, and is converted into an embedding. It is then compared semantically with the current set of medoids, representing the actual email closest to the center of the confirmed emails under that label. The medoid is then recomputed if the similarlity is high enough. For slightly lower confidence, it is marked as suggested, and is at the discretion of the user to confirm that or not. Under confirmation, it triggers a recomputation of the centroid for the user-assigned or confirmed label. After a label medoid reaches a certain number of confirmed samples, it evolves into a k-means clustered distribution. I chose this because semantically, there can be various types of email topics that can fall under a label. For example, there is job offers, recruiting, rejections, and new openings that can all fall under a label for Jobs.

2. Why did you combine BM25 with dense embeddings?

> I chose to combine the embeddings with BM25 because of word weight. Specific words, like LinkedIn, should fall into specific categories like Social Media or Jobs, and using only embeddings would reduce the weight of proper nouns and identifiers that should skew a predicted label.

3. Why did you start with a medoid and later transition to k-means?

> At the beginning, there is no confirmed samples for an email, and the initial classification system is not knowledgeable enough to classify accurately from the get go. Having the behavior transition from user-driven to eventually accurately autonomous is a design choice I wanted to build, that way it would use strict machine learning and avoid LLMs for classification. Additionally, having k-means clusters would account for different subsets of topics within a user-created or pre-set label.

4. Is Labl’s feedback loop reinforcement learning? Why or why not?

> I wouldn't consider it reinforcement learning specifically in today's age because it is not agentic. The feedback loop should ideally improve the accuracy of the system as it is being properly used, but it is strict computed mathematical improvement rather than agent-determined.

5. How would you reformulate Labl as an RL problem?

> I would reformulate Labl as an RL problem by containing it within a test environment and integrating an 

---

## Git-Lint / Coding Agents

1. Walk me through Git-Lint and how it retrieves repository context.

2. What are the main weaknesses of embedding-based retrieval for source code?

3. What happens if Git-Lint retrieves the wrong context or misses the critical dependency?

4. How would you redesign Git-Lint if it became a fully autonomous coding agent?

---

## AI Coding Workflow

1. How do you currently use AI while programming?

2. How do you verify AI-generated code before trusting it?

3. Tell me about a time an AI coding tool produced something that looked correct but was actually wrong or brittle.

4. When would you trust a coding agent to work autonomously, and when would you require human review?

---

## Systems / Ownership

1. What does idempotency mean, and why was it important in your webhook and event-driven systems?

2. Why did you use SQS / queues in your AWS architectures?

3. What did you personally own versus what was already designed by the team?
