# ***Khan Academy First Round Technical Interview Preparation Q+A***

## **Architecture & Design Questions**

1. Why did you choose an orchestration agent + review agent architecture instead of a single monolithic agent? What are the trade-offs, and how does this design help with token limits?
    I originally went with a single API call for each changed file in the diff, running sequentially. However, I wanted to have the comment be added to the pull request as soon as possible in order to minimize waiting time to review the response and make changes. So, I changed to a parallel orchestration agent and review agent architecture. This way, I could have a system in place so that the duration of the entire review would basically be as long as the longest running analysis for a given diff in a file. This also allows for separation of analysis, so the LLM only needs to focus on one source and action per call. However, since the process is now split between multiple agents per diff chunk, it consumes far more tokens. On average, one pull request with decent amount of changes runs around 10-20 cents in API usage. However, it is much faster and more detailed and focused. It also allows for larger diffs to be used, as there is a separation of prompts into multiple different agents rather than all in the same prompt, taking up lots of tokens.

2. Explain your decision to split diffs by file and run reviews in parallel using asyncio.gather(). What would happen if you had a PR with 50 files? How would you handle rate limits or memory constraints?
	Like the answer above, I wanted to make it more temporally efficient through running the reviews in parallel. Instead of executing one after another, they are all started and finished as soon as possible. In a PR with 5-10 files, given that each file may take around 10 seconds to analyze, I would save over a minute and a half with this implementation. The only thing that currently is not implemented is a form of rate limiting. If I had something like 20+ files to review, I would most likely hit the OpenAI rate limiting, since there would be more than 20 requests simultaneously. I did not address this in my beta version because I felt there was no need for it. Since it is for personal use, I never make that many changes per pull request. I prefer to make small feature changes in one specific area and then merge them into the main branch often, to avoid big incompatibility issues and merge conflicts from building up. To address this for possible outside usage, I would add a fixed limit, of something like 10 requests at a time. After implementing this functionality, I could then implement some sort of adaptive limiting later on, increasing and decreasing concurrent requests based on errors or lack thereof, with an exponential backoff to minimize steps until successful backoff.  



3. Why did you choose FastAPI over other frameworks like Flask or Express.js? What specific features of FastAPI made it suitable for this webhook-based architecture?
    I chose FastAPI because it is a lightweight asynchronous framework that fits perfectly for small applications, especially an asynchronous automated one like this. A lot of the processing in this function is done by OpenAI API/Agents SDK, and so there is not much I need to compute within the function itself. FastAPI makes it simple for me to wrap my functions into an application and deploy it, not to mention that it is in Python, which is one of my more comfortable languages. Additionally, I had planned to host the application on AWS Lambda from the beginning given infrequent usage, since I do not open pull requests often. This way, I would save on idle costs. Lambda via Magnum is extremely compatible with AWS Lambda’s event formatting, something that is not as easily implemented with Flask. FastAPI’s BackgroundTasks dependency also makes it simple to run asynchronous tasks. Using something like Express.js would also require a conversion to lambda function, wrapping it in a handler and such.


4. Walk me through the complete data flow from when a PR is opened to when a comment is posted. Include all the async operations, agent calls, and external API interactions. Note: (S) -> synchronous, (A) -> asynchronous
    1. GitHub sends webhook after opening of a pull request (S)
    2. The webhook is parsed to verify signature and correct type of event (S)
    3. The data from the webhook payload is extracted (A)
    4. Tasks are then added to FastAPI BackgroundTasks (S)
    5. The orchestration agent function is then run by BackgroundTasks, beginning the review process (A)
    6. The stored chunk store is then downloaded from S3 for later usage (S)
    7. The diff is then retrieved from the URL (A)
    8. After, it is split based on file (S)
    9. Reviewing tasks are then created for each file (S)
    10. All tasks are then started simultaneously, bounded by the slowest task (A)
    11. In retrieving context, the function used is asynchronous, but has some synchronous parts (A)
    12. The file path is parsed and the file gets chunked into functions (S)
    13. Each chunk is then embedded using OpenAI embedding model (A)
    14. Pinecone is then queried for any closely matching chunks to the current one, and the full text context is looked up in S3 using the hash matching the embedding to its text (S)
    15. The full context is returned, and using that, the review is then handled by the review agent, which calls gpt-4o-mini, waiting for its response and returns it (A)
    16. The summarizer orchestration agent then gathers all the reviews together and makes them into one concise block to get posted as a comment (A)
    17. It is then posted onto the pull request with its GitHub token for authorization (A)
    After the comment is posted, the vector store is updated, first through extracting the changed file paths from the diff (S)
    18. The current file content is then fetched according to the file path (A)
    19. Then, the old chunks for this file are deleted from Pinecone, as well as the local chunk store JSON object (S)
    20. The new file is chunked by function (S)
    21. Each chunk is then embedded again (A)
    22. It is then upserted to Pinecone to replace the old ones (S)
    23. The local chunk store is then synced in with the temp directory chunk store, and that is synced with the chunk store in S3 (S)

5. Why did you use Mangum as the adapter for AWS Lambda? What problems does it solve, and what are the limitations of running FastAPI on Lambda?


## **RAG System & Vector Search Questions**

6. Explain your RAG system architecture in detail. How do you decide what context is relevant for each file being reviewed?

7. Why did you choose Pinecone over other vector databases like Weaviate, Qdrant, or even just using FAISS locally? What specific features of Pinecone were critical?
	Firstly, Pinecone is fully managed by itself. It isn’t as much setup as the others. It automatically manages nearly everything for me. On top of that, Pinecone has very good compatibility with embeddings models from OpenAI, which is what I use (text-embedding-3-small). It also is pretty optimized in retrieval speeds, and comes with easy filtering both before and after, and so I can add in filter settings into my queries very easily. Finally, Pinecone has a generous free tier, which is what I use to store my embeddings without needing to pay out of pocket for a personal project. 

8. Explain the filtering strategy in your Pinecone query (filter={"repo": {"$eq": repo_name}, "path": {"$in": list(file_paths)}}). Why filter by both repo and path?
    I think that this would be the best way to ensure top-level issues and conflicts that may arise from code changes. Although functions used outside of the file path could be affected, issues are more prevalent closer to the file. The filtration by repository is self-explanatory, in that there is no logic in retrieving context from a completely different repository and project.


9. You mention "over 200 code chunks" - how did you determine the chunking strategy? Why split by function/class definitions rather than fixed token sizes?
	I have a py script that manually chunks a repository based on its local version on my laptop, which is where a majority of chunking and uploading occurs. I chose to chunk based on class definition and function because I believe that the entire context of the function is important. Although following fixed token sizes for chunks would be more even throughout, and possibly prevent some chunks from being large, it might not contain enough code to fully understand the context behind the function and how the changes might affect it.

10. In retrieve_context_from_diff(), you set top_k=2 for context retrieval. How did you arrive at this number? What happens if the retrieved context isn't sufficient?
	I chose to go for the top 2 most similar retrieval results since this occurs for each file. Given multiple files changed in a pull request, which is extremely common, there would be 2x retrieved results. To prevent over usage of tokenization, I chose to limit the top k, since the lower ranked results would also not be as contextually relevant. 


11. Your chunking logic uses regex patterns like r"(?=def |class )" for Python. What edge cases might this miss? How would this handle nested classes or decorators?
	


## **OpenAI Agents SDK & Prompting Questions**

12. Why did you use OpenAI's Agents SDK instead of direct API calls to GPT models? What specific benefits does the SDK provide for your use case?
	I chose to migrate to the Agents SDK for future improvements. The biggest benefit that using the Agents SDK has is that I can provide tools for the agent to use. The reason this isn’t currently implemented is because the changes made in my pull requests are not complex enough to require tool usage, and so adding that would not be used. Additionally, I wanted to gain some surface level understanding of how agentic systems work, and so using this helped me get some comprehension on how agents communicate and call each other.


13. Explain the difference between your orchestration agent (using gpt-4o) and review agent (using gpt-4o-mini). Why use different models?
	I used different models to balance performance and reasoning with cost. For review agent usage, I used gpt-4o-mini because there would be a possible number of calls per pull request, in which the token costs could add up. So, I thought 4o-mini would be sufficient to provide well enough analysis and reasoning behind its comments. For the summarization agent, I chose to use gpt-4o since it would be a one time call per pull request. Given that its purpose is to coherently piece together each part of the review while keeping this as concise as possible without losing meaning, I wanted to use a deeper reasoning model. I especially wanted to prevent it from leaving anything out during the concatenation process.


14. Your review agent has very detailed instructions about being "concise" and distinguishing "impactful changes" from "low impact changes." How did you iterate on this prompt? What problems did earlier versions have?
	I iterated on this prompt in my testing rounds. Earlier versions were either unnecessarily verbose, or added detailed analysis for super small changes, like the removal of a comment. The resulting prompt allowed me to retain analysis in the comment for changes that are actually meaningful, with the exception of pull requests with purely, solely a few small changes.



15. How does the Runner.run() method work in the Agents SDK? What's happening under the hood, and how does it differ from a standard chat completion?
    Runner.run() is an abstraction layer that does significantly more than a simple Chat Completion API call. Under the hood, it constructs the conversation context by combining the agent's system instructions with the user prompt, then makes the API call to the specified model. The key difference is that it automatically handles the function calling loop—if the model returns a tool call, Runner executes the function, appends the result to the conversation, and makes another API call until the model returns a final answer without requesting more tools. It also maintains conversation state across multiple turns, so you don't need to manually manage the messages array. The return value is a structured Result object with clean properties like final_output, messages, and function_calls, rather than raw JSON. For my current use case without function calling, it's mostly syntactic sugar that makes the code more readable, but it would save significant boilerplate (~40+ lines) if I added dynamic context retrieval where the agent could autonomously request additional files.



## **AWS & Infrastructure Questions**

16. Walk me through your S3 strategy for storing chunk embeddings. Why not store embeddings directly in Pinecone's metadata or use a traditional database?
    I store the full chunk text (not embeddings, which are in Pinecone) in S3 because Pinecone's metadata has a 40KB size limit per vector, which isn't sufficient for large code chunks like 500-line functions. The chunk store is a JSON file mapping chunk IDs to their full text content, file paths, and chunk IDs—essentially a lookup table. When I retrieve similar chunks from Pinecone, I only get the vector IDs and metadata back, so I use those IDs to fetch the full text from the S3-backed chunk store. A traditional database like PostgreSQL would work, but it adds operational complexity (connection pooling, VPC config for Lambda, database maintenance) for what's essentially a simple key-value lookup. S3 is simpler—no connections to manage, cheap storage ($0.023/GB/month), and Lambda can read from S3 natively in the same region with low latency. The trade-off is that I download the entire chunk store on every cold start rather than querying individual chunks, but for my current scale (200 chunks ≈ 400KB), this is faster than database round trips.



17. Explain the /tmp directory usage in your Lambda function. Why is this necessary, and what are the size limitations?
    AWS Lambda runs in a read-only filesystem except for the /tmp directory, which is the only writable location available to function code. I use /tmp to store the downloaded chunk store JSON file (/tmp/chunk_store.json) and the updated version before uploading back to S3 (/tmp/chunk_s3.json). This is necessary because Lambda's ephemeral nature means I can't write to the deployment package directory or any other location on disk. The /tmp directory has a 512MB storage limit (up to 10GB in newer Lambda configurations), and the storage persists across invocations within the same container (warm starts), but is wiped when the container is recycled. For my use case, the chunk store is typically under 1MB, so this limit isn't a concern. However, if the chunk store grew to 100MB+, I'd need to either increase the /tmp size allocation or implement a different strategy like lazy-loading chunks from S3 on demand rather than downloading the entire store upfront.



18. Your code downloads the chunk store from S3 on every cold start (initialize_chunk_store). How does this impact latency? What happens if the chunk store is very large (e.g., 100MB)?
    Downloading the chunk store on every cold start adds 1-3 seconds to the initial request latency, which is acceptable since the actual review happens in the background and GitHub's webhook already received a 200 response. For warm starts, the global chunk_store variable persists in memory, so subsequent invocations in the same container don't need to re-download. If the chunk store grew to 100MB, the download time would increase to 5-10 seconds depending on network throughput, and it would consume significant memory (Lambda would need at least 512MB-1GB allocated). This would make cold starts noticeably slower and increase costs. To handle large chunk stores, I'd implement lazy loading—store chunks individually in S3 with keys like chunks/{chunk_id}.json, then fetch only the specific chunks returned by Pinecone queries rather than downloading everything upfront. Alternatively, I could use DynamoDB for chunk storage, which would allow efficient single-item queries without loading the entire dataset into memory.



19. In update_file_embeddings(), you delete old chunks and upsert new ones for modified files. What happens if this process fails halfway through? How would you make this more resilient?
    If the process fails halfway through, I could end up in an inconsistent state—old chunks deleted from Pinecone but new chunks not yet inserted, or Pinecone updated but S3 not updated with the new chunk store. This would cause missing context in future reviews for those files. The current code has no transactional guarantees or rollback mechanism. To make this resilient, I'd implement a two-phase approach: first, create all new chunks and upsert them to Pinecone with temporary IDs, then delete the old chunks only after confirming the new ones are successfully indexed. I'd also wrap the S3 upload in a try-except and implement retries with exponential backoff. For production, I'd add a "version" field to each chunk and use optimistic concurrency control—never delete old versions until new versions are confirmed. Another approach would be event sourcing: log all changes to an append-only log (like DynamoDB Streams or Kinesis), then process updates asynchronously with dead-letter queues for failures, allowing retries without losing data.



20. You're using background tasks in FastAPI (background_tasks.add_task). How does this interact with Lambda's execution model? What happens if Lambda kills the container before the background task completes?
    FastAPI's background tasks run after the HTTP response is sent but before the Lambda invocation completes, which works because Mangum (the ASGI adapter) keeps the Lambda execution context alive until all async tasks finish. Lambda waits for the event loop to drain before terminating the invocation, so background tasks will complete as long as they finish before the Lambda timeout (15 minutes max). However, if the task exceeds the timeout, Lambda forcibly kills the container and the task is lost—there's no built-in retry or persistence. This is a potential issue for long-running reviews (e.g., 50-file PRs taking 2+ minutes). A more robust approach would be to use Step Functions for orchestration, or push the task to an SQS queue and have a separate Lambda (or ECS task) consume it. That way, if the webhook handler times out, the review job persists in the queue. For the current design, I'm relying on typical PRs completing in under 60 seconds, and accepting that edge cases (huge PRs, slow OpenAI responses) might fail silently. Adding CloudWatch alarms on Lambda errors would help detect these failures.



# Code-Specific Deep Dives

21. In chunk_diff(), you use re.split(r"^diff --git.+?^(@@.+?@@)", diff, flags=re.MULTILINE | re.DOTALL). Explain this regex pattern and why you need both MULTILINE and DOTALL flags.
    The pattern r"^diff --git.+?^(@@.+?@@)" is trying to split on both diff --git headers (which mark file boundaries) and @@ hunk headers (which mark changed sections within files). The ^ anchors match the start of a line, .+? is a non-greedy match of any characters, and the pattern captures the @@ hunk header in a group. MULTILINE makes ^ match the start of each line in the diff (not just the start of the entire string), which is necessary since diff --git and @@ appear on their own lines. DOTALL makes . match newline characters, allowing .+? to span multiple lines between diff --git and the next @@. Without MULTILINE, the regex wouldn't match mid-string occurrences of these markers; without DOTALL, it wouldn't capture multi-line blocks. However, I think this regex might be overly complex and could produce unexpected splits—a simpler approach would be to split only on diff --git or only on @@ depending on the granularity needed. The current pattern might create malformed chunks if the diff structure is unusual.



22. Your split_diff_by_file() function has a try-except block that silently continues on IndexError. What scenario causes this error, and is it safe to skip?
    The IndexError occurs when header_line.split(' b/')[1] fails because the diff header doesn't have the expected format a/path b/path. This can happen with binary files, deleted files, or unusual git diff formats (e.g., diff --git a/file b/file without the space before b/). By using continue, I'm silently skipping files that don't match the expected format, which could mean the review misses important changes. Whether it's safe depends on context—if these are always binary files or irrelevant assets, it's fine. But if it's a legitimate code file with an unusual diff format, skipping it is a bug. A better approach would be to log a warning when this happens (e.g., logger.warning(f"Skipped malformed diff header: {header_line}")) so I can investigate which files are being dropped. I could also add a fallback parser that tries alternative extraction methods before giving up. For production, I'd track metrics on how often this occurs to understand if it's a real issue or just noise from binary files.



23. Explain the purpose of the hash_content() function in your embeddings pipeline. Why hash chunks, and how does this prevent duplicate embeddings?
    The hash_content() function uses SHA-256 to create a deterministic fingerprint of each chunk's text content. I use this hash as part of the chunk ID (e.g., file.py-0-abc123def) to uniquely identify each chunk's content. This prevents duplicate embeddings in two ways: first, when initially building embeddings, I cache hashes of already-embedded chunks, so if the same code appears multiple times (e.g., copy-pasted functions), I only embed it once. Second, when updating embeddings after a PR, I can detect if a chunk's content actually changed—if the hash matches an existing chunk, I skip re-embedding and re-upserting to Pinecone, saving API costs and avoiding unnecessary writes. Without hashing, I'd need to do expensive string comparisons to detect duplicates, or risk embedding the same content multiple times under different IDs. The hash also serves as a content-addressable identifier, similar to how Git uses SHA hashes for commits—two chunks with identical content will always have the same hash, enabling deduplication across the entire codebase.



24. In update_file_embeddings(), you fetch file content from https://raw.githubusercontent.com/kylehton/{repo_name}/main/{file_path}. What happens if the PR is against a different branch? Is this a bug?
    Yes, this is absolutely a bug. I'm hardcoding /main/ in the URL, which means if a PR is opened against a develop or feature branch, I'll fetch the wrong version of the file—I'll get the main branch version instead of the actual updated content from the PR's head branch. This would cause the embeddings to be out of sync with what was actually changed in the PR. To fix this, I need to extract the head branch from the webhook payload (it's in data["pull_request"]["head"]["ref"]) and use that in the URL: f"https://raw.githubusercontent.com/{repo}/{head_ref}/{file_path}". Alternatively, I could use the GitHub API's Contents endpoint (GET /repos/{owner}/{repo}/contents/{path}?ref={sha}) with the specific commit SHA from the PR head, which would be more reliable since branch names can be ambiguous. This is a critical fix for production—without it, my embedding store would diverge from the actual codebase state after non-main PRs are merged.



25. Your global variable chunk_store is mutated throughout the application. How does this work in a Lambda environment where multiple invocations might run concurrently?
    In Lambda, each container instance has its own isolated memory space, so the global chunk_store variable is not shared across concurrent invocations—each invocation gets its own copy. However, within a single container, the variable persists across warm invocations, which is actually beneficial for performance (avoids re-downloading from S3). The potential issue arises if two invocations happen simultaneously and AWS spins up two containers—they each download the chunk store independently, then both might update it and upload to S3, causing a race condition where the last write wins. If PR #1 updates file_a.py and PR #2 updates file_b.py at the same time, whichever uploads to S3 last will overwrite the other's changes, potentially losing embeddings. To fix this, I'd implement optimistic concurrency control: include a version number or timestamp in the chunk store, download it before uploading, merge changes, and use S3's conditional writes (e.g., If-Match headers with ETags) to detect conflicts. Alternatively, I could use DynamoDB with conditional writes per chunk instead of a single JSON file, eliminating the whole-file race condition.



## **Error Handling & Edge Cases**

26. What happens if OpenAI's API is down or rate-limits you during a review? How would you detect and handle this?
    Currently, if OpenAI's API is down or returns a 429 rate limit error, the async call to Runner.run() or embeddings.create() would raise an exception, which would propagate up and cause the entire background task to fail silently—no review gets posted, and the user never knows what happened. There's no retry logic, exponential backoff, or error notification. To detect this, I'd wrap API calls in try-except blocks that catch openai.RateLimitError and openai.APIError, log the errors to CloudWatch, and implement exponential backoff retries using a library like tenacity (e.g., @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))). For rate limits specifically, I'd also add adaptive throttling—use a semaphore to limit concurrent API calls (e.g., max 10 at once) and dynamically reduce concurrency when 429 errors occur. If retries exhaust, I'd post a fallback comment to the PR like "Code review failed due to temporary API issues—please re-trigger" so users aren't left in the dark. I'd also set up CloudWatch alarms to notify me when error rates exceed thresholds.



27. Your webhook handler only processes PRs with action == "opened". Why not handle "synchronize" (new commits pushed) or "reopened"?
    I only handle action == "opened" to keep the initial implementation simple—each PR gets reviewed exactly once when first opened. However, this means that if a developer pushes new commits to the PR (action synchronize), those changes aren't reviewed, which significantly limits usefulness. Handling synchronize would mean reviewing incremental changes, which adds complexity: I'd need to diff only the new commits since the last review, not the entire PR. Without this, developers could push buggy code after the initial review passes. Not handling reopened is less critical but still a gap—if a PR is closed then reopened, it won't get re-reviewed even if content changed. To support these actions, I'd check if action in ["opened", "synchronize", "reopened"] and track which commits were already reviewed (maybe store the last reviewed SHA in PR metadata or a database). For synchronize, I'd fetch the incremental diff using GitHub's compare API: GET /repos/{owner}/{repo}/compare/{base}...{head}. This would make the system production-ready.



28. What happens if a PR diff is extremely large (e.g., 10,000 lines across 100 files)? How would you prevent timeouts or excessive costs?
    With 100 files, I'd hit several bottlenecks: first, firing 100 concurrent review agent calls would almost certainly exceed OpenAI's rate limits (500 RPM for most tiers), causing failures. Second, the summarizer agent would receive 100 reviews as input, likely exceeding the 128K token context window. Third, updating 100 files' embeddings could take 3-5 minutes, risking Lambda timeouts. Fourth, the cost would be ~$2-3 per PR instead of $0.01-0.02. To prevent this, I'd implement several safeguards: add a file count limit (e.g., only review PRs with ≤20 files), and for larger PRs, post a comment saying "PR too large for automatic review—recommend breaking into smaller changes." I'd also add filtering to skip trivial files (e.g., only review files with >10 lines changed) and prioritize important file types (skip generated code, lockfiles, assets). For concurrency, I'd use a semaphore (max 10 concurrent reviews) to avoid rate limits. For costs, I'd add a budget check—estimate tokens before starting and abort if projected cost exceeds a threshold. Finally, I'd add a Lambda timeout guard that saves partial progress if approaching the 15-minute limit.



29. Explain the potential race condition in your embedding update process. What if two PRs are opened simultaneously for the same repository?
    If two PRs are opened simultaneously, AWS will spin up two Lambda containers, each of which downloads the chunk store from S3, makes its own updates, and uploads back to S3. The race condition occurs because both containers are working with stale versions of the chunk store—neither knows about the other's changes. For example, if PR #1 updates fileA.py and PR #2 updates fileB.py, both download the chunk store, modify their respective files' chunks, then upload. Whichever uploads second will overwrite the first upload, potentially losing the first PR's embedding updates. The Pinecone updates might succeed for both (since they're keyed by chunk ID), but the S3 chunk store would only reflect the last write. This creates an inconsistency where Pinecone has embeddings that aren't in the S3 chunk store, or vice versa. To fix this, I'd use optimistic locking: store a version number in the chunk store JSON, and before uploading, re-download the latest version, merge my changes with any new changes, increment the version, and upload. Alternatively, use DynamoDB with conditional writes (UpdateItem with condition expressions) to update individual chunks atomically instead of one big JSON file.



# Performance & Optimization Questions

30. You're making sequential embedding calls in update_file_embeddings() for each chunk. Why not batch these? How would you optimize this for large files?
    I'm making sequential embedding calls because I wrote the code with simplicity in mind—each chunk gets embedded one at a time in a for loop. This is inefficient because OpenAI's embeddings API supports batching up to 2,048 inputs in a single request, which would dramatically reduce latency and cost. For a file with 10 chunks, sequential calls take ~10 × 300ms = 3 seconds, whereas a single batched call would take ~500ms. To optimize, I'd collect all chunk texts for a file, make one batched embedding call (openai.embeddings.create(input=[chunk1, chunk2, ...])), then map the returned embeddings back to their respective chunks. For very large files (e.g., 100+ chunks), I'd batch in groups of 100 to stay within API limits and memory constraints. I'd also parallelize embedding across files—instead of processing files sequentially in update_file_embeddings(), use asyncio.gather() to embed multiple files concurrently. This would reduce the embedding update phase from 20-30 seconds to 5-10 seconds for typical PRs. The trade-off is slightly more complex error handling (need to handle partial batch failures), but the performance gain is worth it for production.



# **Comprehensive Project Breakdown**

## *System Architecture Overview*

The Git-Lint project is a serverless, event-driven AI code reviewer that leverages an orchestration agent pattern with RAG-based context retrieval. Here's the complete flow:

1. Webhook Reception: GitHub sends a webhook when a PR is opened → FastAPI endpoint receives it
2. Background Processing: Review task is offloaded to background to avoid GitHub webhook timeout (10s)
3. Chunk Store Initialization: Downloads pre-computed code embeddings from S3 to /tmp
4. Diff Retrieval: Fetches the unified diff from GitHub via the diff_url
5. Parallel File Processing: Splits diff by file, then for each file:
- Chunks the diff text into embeddable pieces
- Embeds each chunk using text-embedding-3-small
- Queries Pinecone for the top 2 most similar code chunks (filtered by repo + file path)
- Passes file diff + retrieved context to review agent (gpt-4o-mini)
6. Aggregation: Orchestration agent (gpt-4o) synthesizes all file reviews into one cohesive comment
7. Posting: Comment posted to PR via GitHub API
8. Embedding Update: Modified files are re-chunked, re-embedded, and Pinecone is updated; S3 is updated with new chunk store

## *Key Technical Components*

1. Orchestration Agent (gpt-4o)
- Purpose: Synthesize multiple file-level reviews into a single PR comment
- Why separate from review agent: Different skill required—summarization vs. detailed analysis
- Trade-off: Extra API call but better quality output

2. Review Agent (gpt-4o-mini)
- Purpose: Analyze individual file diffs with context
- Model choice: Cost optimization—mini is 15-20x cheaper than gpt-4o
- Prompt engineering: Highly constrained to avoid verbosity and focus on impactful changes

3. RAG System
- Vector DB: Pinecone (managed, serverless, scalable)
- Embedding Model: text-embedding-3-small (1536 dimensions, $0.02/1M tokens)
- Chunking Strategy: Language-aware splitting at function/class boundaries
- Context Retrieval: Semantic search with metadata filtering (repo + file path)
- Chunk Storage: S3 for persistent storage, /tmp for Lambda runtime access

4. FastAPI + Mangum + Lambda
- FastAPI: Modern async framework with automatic OpenAPI docs
- Mangum: ASGI adapter that translates AWS Lambda events to ASGI format
- Lambda: Serverless compute—pay per invocation, auto-scaling
- Trade-off: Cold starts (~2-3s) but cost-effective for low-traffic webhooks

## *Critical Design Decisions*

Why Async Everywhere?
- GitHub webhook timeout is 10 seconds
- Background tasks allow immediate 200 response
- asyncio.gather() enables parallel file reviews (5 files reviewed simultaneously vs. sequentially)

Why S3 for Chunk Store?
- Pinecone metadata has size limits (40KB per vector)
- Full chunk text can be large (functions with 500+ lines)
- S3 is cheap ($0.023/GB/month) and fast enough for cold start reads

Why Delete + Reinsert Embeddings?
- File modifications invalidate old embeddings
- Simpler than partial updates (which would require tracking line-level changes)
- Trade-off: Higher API costs but correct semantics

Why Filter by File Path in Pinecone Query?
- Dramatically reduces search space (200+ chunks → ~5-10 chunks per file)
- Ensures context is from the same file being reviewed (high relevance)
- Without filtering, you'd get random snippets from the entire codebase

## *Potential Weaknesses & Interview Follow-ups*

1. No retry logic: If OpenAI fails, the review silently fails
2. No rate limiting: Concurrent PRs could exhaust API quotas
3. Hardcoded GitHub username: kylehton is hardcoded in get_file_content()
4. Branch assumption: Always fetches from main branch, not the PR's source branch
5. No deduplication: Same file modified in multiple PRs → redundant embedding updates
6. Global state: chunk_store could cause issues in concurrent Lambda executions (though unlikely due to Lambda's execution model)
7. No monitoring: No CloudWatch metrics, no error alerting

## *Cost Analysis*

For a typical PR with 5 files:
- Embeddings: 5 files × 10 chunks × $0.02/1M tokens ≈ $0.001
- Review agent: 5 calls × 1000 tokens × $0.15/1M tokens ≈ $0.0008
- Orchestration agent: 1 call × 2000 tokens × $5/1M tokens ≈ $0.01
- Pinecone: 50 queries × $0.0004/1K queries ≈ negligible
- Total per PR: ~$0.012

## *What Makes This Project Strong*

- Real production system: Handles actual GitHub webhooks
- Multi-agent orchestration: Demonstrates understanding of agentic patterns
- RAG implementation: Full pipeline from chunking → embedding → retrieval → augmentation
- Cloud-native: Properly leverages Lambda, S3, Pinecone (not just running locally)
- Async programming: Proper use of asyncio for performance
- Cost optimization: Strategic use of gpt-4o-mini vs. gpt-4o

## *Key Talking Points*

1. "Why agents over RAG alone?": Agents provide iterative reasoning and can handle multi-step tasks (review → summarize → post)
2. "How does this scale?": Parallel file processing + serverless architecture means it scales horizontally automatically
3. "Future improvements?": Add streaming responses, implement retry logic, add observability, support multi-repo configuration


## *Architecture end-to-end*

The system is event-driven: GitHub emits a pull_request webhook to a FastAPI endpoint exposed via API Gateway. The handler validates the event, extracts the repo name, diff_url, and issue_url, and immediately enqueues a background task so the webhook can return 200 quickly. The background task initializes context by downloading the code-chunk store from S3 into /tmp, then fetches the PR diff via the diff_url. The diff is split by file, and per-file review tasks are launched in parallel with asyncio.gather; each task retrieves semantic context from Pinecone and calls the Review Agent to analyze only that file’s changes. When all file reviews finish, the Orchestrator Agent synthesizes them into a coherent PR comment and the service posts it back to GitHub. Finally, the system re-chunks and re-embeds modified files, upserts vectors into Pinecone, updates the local chunk store, and uploads the refreshed store to S3. Logs and errors flow to CloudWatch, while artifacts (the chunk store) live durably in S3 and vectors in Pinecone.

## *Component interaction (Lambda, FastAPI, Pinecone, S3, OpenAI Agents SDK)*

FastAPI (ASGI) runs inside Lambda via Mangum, translating API Gateway events into ASGI requests. S3 holds the authoritative “chunk store” (full text of code chunks keyed by ID) that the Lambda downloads to /tmp and later uploads after updates. Pinecone stores vector embeddings for those chunks, enabling filtered similarity search (by repo and file path) that powers the RAG context passed to the Review Agent. The OpenAI Agents SDK executes two roles: the Review Agent (file-level analysis using retrieved context) and the Orchestrator Agent (synthesis across files into one comment). GitHub’s REST API is used to fetch diffs and post PR comments; httpx handles async HTTP. The data path is webhook → Lambda/FastAPI → GitHub diff → Pinecone semantic search → Agents SDK for review/summarization → GitHub comment, with S3 as durable state and Pinecone as retrieval memory. Concurrency is primarily at the “per-file review” step, while updates to embeddings run sequentially today.

## *Why Lambda instead of EC2 or ECS*

Lambda fits an event-driven webhook workload with bursty, short-lived compute, so you only pay per invocation and scale to zero between PRs. It removes server management and autoscaling concerns you’d shoulder on EC2 or ECS, and cold starts are acceptable because the webhook returns immediately while work continues asynchronously. Packaging as a Lambda function via Mangum is straightforward and avoids maintaining container clusters or long-lived instances. AWS handles multi-AZ resiliency automatically, which is overkill to re-create on EC2 for a sidecar review service. For small to medium traffic, Lambda’s cost model is materially cheaper than an always-on EC2/ECS footprint. The trade-offs (ephemeral disk, statelessness, timeouts) are manageable here because persistent state is externalized to S3 and Pinecone, and the heavy lift is I/O-bound. If traffic or processing windows grew dramatically, ECS/Fargate would be my next step for long-running or batched jobs.

## *Handling concurrent requests and scaling limits in Lambda*

Lambda scales horizontally by spinning up additional containers per concurrent invocation up to your account’s concurrency limit; API Gateway can fan in requests effortlessly. Internally, I keep per-invocation concurrency under control with asyncio.gather for parallel reviews and would cap OpenAI/Pinecone calls with a semaphore to avoid upstream rate limits. Reserved concurrency can be configured to protect downstream services from overload, and provisioned concurrency can mitigate cold starts during peak hours. Timeouts are set below 15 minutes; if a PR risks overrunning, I would batch files or push the job to an SQS-driven worker Lambda. To guard against throttling, I’d implement retries with exponential backoff and adaptive throttling that reduces concurrency on 429s. Observability from CloudWatch metrics and structured logs helps detect saturation early. In practice, the system scales on two axes: Lambda concurrency for ingress and bounded fan-out for per-file reviews.

## *Managing state in a stateless Lambda*

All durable state is externalized: vectors live in Pinecone; the authoritative chunk store (full text) lives in S3; GitHub is the source of truth for repository content. The only in-memory state is the deserialized chunk store and per-request review artifacts; these persist for the life of a warm container but are re-created on cold starts. For cross-invocation coordination, S3 acts as the write-through store—after embedding updates, the chunk store JSON is written to /tmp and uploaded to S3. Because multiple Lambdas can race on writes, I would add optimistic concurrency (ETag conditional PUT or version fields) to merge changes atomically. Idempotency is achieved by deterministic chunk IDs (include content hash) so repeated runs won’t duplicate vectors. Any long-running orchestration can be pushed to queues/Step Functions to make progress resilient across invocations. This pattern keeps Lambdas stateless while maintaining a consistent external state graph.

## *Improvements if I had more time*

I’d harden reliability: add batched embeddings, retry/backoff, and a semaphore-based rate limiter to guard OpenAI/Pinecone. I’d address correctness gaps by fetching file contents from the PR head SHA (not main) and adding optimistic locking for S3 updates to avoid last-write-wins. I’d parallelize the embedding update phase across files and batch chunks per file to cut latency by 3–5×. For scale, I’d move long-running reviews to SQS/Step Functions and have the webhook handler become a pure enqueuer with durable progress tracking. I’d switch Python regex chunking to AST/tree-sitter for semantically correct chunk boundaries and better decorator/nesting handling. Observability would include structured logs, tracing, and metrics (review time, cost, retrieval hit rates). Finally, I’d add an opt-in “auto-fix” mode that proposes patches and opens suggested commit PRs.

## *OpenAI Agents SDK: structuring reasoning/memory*

I model two agents: a file-level Review Agent constrained to concise, impact-focused feedback, and an Orchestrator Agent that synthesizes file reviews into a cohesive PR comment. Each agent is initialized with role instructions that bias behavior (avoid verbosity, focus on impactful changes, produce structured markdown). The Review Agent’s prompts include the diff plus retrieved context snippets to emulate “memory” of relevant parts of the repo without exceeding token limits. I avoid long transcripts; each call is largely single-shot with carefully curated context, which improves determinism and cost. If extended, I’d enable tool-calling so the agent can fetch missing symbols or neighboring files on demand, then cache those fetches. I would also track retrieval metadata so the orchestrator can cite where insights originated. The separation of roles reflects distinct reasoning tasks—analysis versus summarization.


## *OpenAI Agents SDK: handling context size/token limits*

I constrain context by retrieving a small, filtered set of chunks (top_k=2 per diff chunk) restricted to the same repo and file paths to avoid noise. Each file is reviewed in its own call, effectively multiplying available context across files and preventing a single monolithic prompt from hitting the model’s window. If I approach limits, I would truncate low-salience sections (e.g., unchanged or formatting-only hunks) and cap the number of context chunks or their total tokens. Ahead-of-call token estimation via tiktoken could enforce a hard ceiling with a buffer for the model’s output. For large PRs, batching or staged passes (quick high-level pass then deeper follow-up where needed) keeps prompts within budget. Summarization is a separate call with controlled inputs to stay under limits. If needed, I’d pivot to a higher-window model only for the summarization step.

## *OpenAI Agents SDK: prompting and constraining behavior*

Prompts explicitly differentiate impactful changes (logic, behavior, API, performance) from low-impact ones (formatting, comments), with instructions to keep non-impactful items brief and consolidate feedback. I use imperative, testable directives—“return only changed lines with explanations, no diff syntax”—to minimize model drift. Role naming (“Review Agent”, “Summarizer Agent”) and audience framing (“direct, precise, actionable feedback”) reduce verbosity and fluff. I pass file path and minimal but targeted context to anchor the model in a specific locus of code. The orchestrator gets a clearly delimited set of file reviews and a synthesis instruction, producing a single PR comment instead of per-file spam. If hallucinations appeared, I would add guard-rails like “do not infer unobserved code,” ask for uncertainty flags, or require citations back to retrieved chunks. Temperature remains low to encourage determinism.

*OpenAI Agents SDK: preventing hallucinations/irrelevant suggestions*

I reduce hallucinations by limiting context strictly to retrieved chunks tied to files present in the diff, and by forbidding speculation about unseen code. The instructions ask the model to defer when context is insufficient and suggest what additional files would help, rather than fabricate. Retrieval is filtered by repo and file path, raising the prior that returned chunks are relevant neighbors of the diff. For consistency, I’d add a minimal confidence heuristic based on Pinecone similarity; below a threshold, fetch additional context or mark feedback as tentative. I also discourage broad refactors unless justified by concrete changes in the diff. In future, tool-calling to fetch specific symbol definitions on demand would further reduce guesswork. Finally, I’d log representative prompts/outputs to spot patterns of drift and tighten prompts iteratively.

## *Pinecone: creating and updating embeddings when code changes*

Initial indexing chunks code per language-aware regex, embeds each chunk with text-embedding-3-small, and upserts vectors with metadata (repo, path, chunk_id, preview, hash). The full text of each chunk is stored in S3 and keyed by the same ID, enabling the review flow to reconstruct complete context from Pinecone matches. On PRs, I extract modified file paths, delete prior vectors for those files, re-chunk current file contents, embed the new chunks, and upsert them back. The local chunk_store is updated and then uploaded to S3, keeping vector IDs, metadata, and full text synchronized. Hashes allow me to skip unchanged content, reducing cost. Today this update phase is sequential; I’d batch and parallelize it. Optimistic concurrency on the S3 store prevents races between simultaneous PRs.

## *Pinecone: query strategy for relevant context*

For each diff chunk, I compute an embedding and query Pinecone with top_k limited (default 2), include_metadata=True, and a metadata filter that pins to the repo and narrows to paths extracted from the diff. This filter keeps results local to touched files and their neighbors, improving precision and token efficiency. I then resolve match IDs back to full text using the chunk store and concatenate several top matches into the prompt. If similarity scores were exposed and low, I would expand scope from exact paths to directories or modules to capture related utilities. When diffs are small or trivial, retrieval returns few or no matches, and the agent falls back to a minimal-context review. For robustness, I’d add caching for frequent queries and batch queries when processing many chunks. Monitoring hit rates helps tune top_k and filters.

## *Pinecone: embedding model choice*

I use text-embedding-3-small for its strong cost-to-quality ratio and wide adoption; it’s sufficient for code retrieval at the function/method granularity with concise chunks. Compared to larger embedding models, it keeps token costs low during both indexing and query-time embeddings. The 1,536-d vector size is compatible with Pinecone and performs well in practice for cross-lingual code/text. If evaluations showed retrieval misses, I’d test code-specific models or larger variants and A/B the impact on review quality. I also ensure consistent preprocessing (strip, length threshold) for stable embeddings. The model choice supports scaling without cost spikes on busy repos.

## *Why Pinecone over Weaviate/Qdrant*

For a serverless pipeline, Pinecone’s fully managed operations and simple API reduce the operational burden—no cluster sizing, backups, or upgrades. Cold-start Lambda invocations benefit from a hosted endpoint with predictable latency rather than a self-managed vector service. Weaviate and Qdrant are excellent, especially self-hosted or in VPCs, but they add infra complexity (networking, patching, HA) that’s disproportionate for a webhook worker. Pinecone’s metadata filtering and namespaces meet my needs without custom schema wrangling. If I needed on-prem, hybrid, or lower-level control, I’d revisit those options. For cost-sensitive large scale, I’d also benchmark Qdrant’s managed offering. Today, Pinecone’s simplicity and reliability win.

## *AWS Lambda: packaging dependencies*

I package the service with the AWS Lambda Python base image and install requirements.txt at build time, copying the app and setting the handler to main.handler via Mangum. This yields a predictable, reproducible container compatible with Lambda’s execution environment. Using the Lambda base image avoids glibc or manylinux mismatches that can occur with native deps. If I needed faster cold starts, I’d minimize dependencies, strip unused transitive packages, and consider Lambda Layers for shared libs. For very heavy deps, I’d prebuild wheels and vendor them. The image is small enough for quick deploys while retaining ASGI support.

## *AWS Lambda: handling cold starts*

Cold starts involve container provisioning, module import, and chunk store download; I mitigate user-facing latency by responding to the webhook immediately and doing heavy work in the background task. Provisioned concurrency could keep a small pool warm during business hours, trading small fixed cost for predictable latency. I keep imports lean and defer non-essential initialization until needed (e.g., downloading the chunk store only when processing reviews). For long processes, moving the job to SQS ensures progress even if a container is recycled. Observability tracks cold vs warm invocation times. Tuning memory can reduce cold start time because Lambda allocates CPU proportional to memory.

## *AWS Lambda: deployment and monitoring*

I would deploy via a simple CI step building the image, pushing to ECR, and updating the Lambda function; infrastructure can be scripted with SAM/CDK/Terraform. API Gateway integrates with Lambda, and route mapping exposes /review. Monitoring relies on CloudWatch Logs for structured app logs, metrics for invocations/errors/duration, and alarms for error spikes or throttles. X-Ray could trace external calls (OpenAI, Pinecone, GitHub) to identify bottlenecks. Dead-letter queues capture failed invocations for later inspection. For performance, I track review duration and cost estimates to catch regressions.

## *AWS Lambda: concurrency model and timeout*

Concurrency scales per incoming request; I’d set reserved concurrency to a safe number so I don’t overwhelm OpenAI/Pinecone and apply semaphores inside the handler to bound fan-out. The timeout is set to a few minutes to comfortably cover typical PRs; any longer-running work belongs in a queue/worker model. If concurrency bursts exceed external rate limits, retries with exponential backoff and jitter handle transient errors. Provisioned concurrency smooths latency for predictable spikes. I’d log per-file timing to understand saturation points. Backpressure is applied at the per-file review layer.

## *FastAPI: endpoint structure*

The service exposes GET / for health and POST /review to receive GitHub webhooks. The handler inspects X-GitHub-Event, handles ping quickly, and for pull_request events extracts the action, diff_url, issue_url, and repo metadata. For “opened” events, it schedules a background task to run the orchestration agent and responds immediately to avoid webhook timeouts. Inputs are parsed from the JSON payload; response is a lightweight confirmation message. Errors on unknown events return a benign message without raising 500s. The critical behavior is to decouple webhook responsiveness from review processing.

## *FastAPI: async I/O and background tasks*

All network I/O (GitHub, OpenAI, Pinecone) is async via httpx and the Agents SDK, enabling concurrency with asyncio.gather across files. BackgroundTasks lets the handler return while the review continues in the same invocation, keeping control simple while avoiding the need for an external queue. Per-file tasks run concurrently; I’d add a semaphore to cap concurrency for rate limits. The orchestrator and summarization are also awaited within the background task. This approach balances responsiveness and simplicity but remains bounded by the Lambda timeout. For higher reliability, I’d promote background work to SQS.

## *FastAPI: input validation and error handling*

I validate event type and action and short-circuit non-PR events; malformed payloads would be handled with safe dict access and logged rather than crashed. For production, I’d add Pydantic models for the GitHub payload subset I use, enabling explicit field validation. Downstream API errors are caught and logged with enough context (repo, PR number) to debug. User-facing responses never leak internal errors; instead, the system posts a friendly failure comment if reviews can’t be produced. Idempotency can be enforced with GitHub delivery IDs to avoid double-processing. Structured logging (JSON) makes failures queryable.

## *Biggest integration challenges*

The hardest parts were getting reliable diff parsing across file types, ensuring retrieval returned truly relevant context, and preventing token bloat. Balancing concurrency to speed up reviews without tripping OpenAI or Pinecone rate limits required careful orchestration. Keeping S3 and Pinecone in sync across updates—and anticipating races from concurrent PRs—forced discipline around deterministic IDs and planned concurrency control. Lambda’s statelessness demanded that I design state flows explicitly, which paid off later for reliability. Prompt design took iteration to reduce verbosity and focus only on impactful changes. Finally, making the system resilient to partial failures (e.g., some file reviews succeed, others fail) was a key design goal.

## *Why Pinecone instead of a relational database*

Relational databases excel at structured queries and transactions, not high-dimensional vector similarity search at scale. Pinecone gives managed, low-latency vector search with metadata filtering and horizontal scaling out of the box. While I could store chunk text in Postgres and run FAISS locally, that complicates serverless deployments and stateful hosting. For Lambda, an external managed vector service simplifies operations and avoids cold-starting an index. The metadata I need (repo, path, chunk_id) maps cleanly to Pinecone filters. If I needed joins, analytical queries, or transactional updates across entities, I’d pair Pinecone with a relational store; here, S3 suffices for chunk text.

## *What breaks if OpenAI latency spikes*

Longer model latency stretches the per-file review step and can push total processing toward the Lambda timeout, risking abrupt termination before posting comments. High latency also increases the chance of rate-limit retries colliding with timeouts. The summarization step is another single-call bottleneck—if it stalls, no final comment is produced even if all file reviews succeeded. To mitigate, I’d set generous but safe timeouts, add partial-result posting (e.g., per-file comment fallback), and move execution to SQS/Step Functions to decouple duration from API Gateway lifecycles. Caching retrieval and reusing embeddings reduces dependence on LLM calls. Monitoring P95/P99 latency would trigger adaptive concurrency reductions.

## *Ensuring consistent embeddings across updates*

Consistency comes from deterministic IDs that include file path, chunk index, and content hash, ensuring one unique vector per semantic unit. Before inserting new chunks, I delete existing vectors for the file, then upsert the fresh set; the chunk store is updated in lockstep and uploaded to S3. To avoid races, I’d add versioning or ETag conditions to the S3 upload so parallel updates merge instead of overwriting. Hashes let me skip re-embedding unchanged chunks to reduce drift and cost. Periodic reconciliation can compare Pinecone IDs to the S3 store and repair mismatches. Logging every delete/upsert with counts provides an audit trail.

## *Handling OpenAI rate limits*

I would wrap API calls with exponential backoff and jitter, detect 429s explicitly, and reduce concurrent requests via a semaphore (adaptive throttling drops concurrency when errors spike). Requests are already sharded per-file; batching smaller files together can reduce call counts. I’d preflight budget and estimated tokens for very large PRs and bail out early with a user-facing message if limits would be exceeded. For throughput, I’d reuse connections and keep prompts lean. If constraints persist, I’d queue overflow work and process asynchronously, posting status updates to the PR.

## *Testing locally*

I test the FastAPI app with pytest and httpx’s AsyncClient to exercise the /review endpoint using recorded GitHub payloads. Diff parsing, file splitting, and path extraction are unit-tested with representative diffs, including binary and rename cases. Retrieval is tested with a local or stubbed Pinecone client and a small synthetic index; OpenAI calls are mocked to return canned reviews and embeddings. For end-to-end testing, I replay a sample PR against a sandbox repo and assert that a comment is posted. I validate error paths by forcing timeouts and 429s to ensure retry and fallback logic behaves. Finally, I add golden-file snapshot tests to keep prompt formats stable.


## *Verifying AI-generated reviews*

I check structural constraints first (conciseness, presence of changed-line references, summary at end). I sample outputs and compare against a rubric: did it prioritize impactful changes, avoid nitpicks, and refrain from fabricating context? I also measure developer feedback: reactions on PR comments and acceptance rate of suggested improvements. For regression, I keep example diffs and expected review characteristics to catch drift from prompt edits. Over time, I’d compute simple quality metrics (e.g., fraction of comments later revised or dismissed). When confidence is low, the agent is instructed to state uncertainty or ask for additional context.

## *Handling failed API calls or embedding errors*

All outbound calls should be wrapped with retries and circuit-breaker semantics; transient failures get exponential backoff, while persistent failures bubble up and trigger a graceful fallback. If a single file review fails, I still proceed with others and annotate the final comment with a note that some files could not be reviewed. If embedding updates fail, I avoid deleting existing vectors until new ones are confirmed inserted to prevent data loss. Errors are logged with correlation IDs (repo/PR/commit) and surfaced via CloudWatch alarms. For repeated failures, I’d add a dead-letter queue to capture jobs for later reprocessing. The guiding principle is partial progress over all-or-nothing.

## *Monitoring and logging*

I emit structured JSON logs with stages (diff_fetch, retrieval, review, summarize, post_comment, embeddings_update), durations, and counts per stage. CloudWatch metrics track invocation count, errors, duration, OpenAI/Pinecone error rates, and similarity-score distributions to gauge retrieval quality. Alarms notify on elevated 4xx/5xx, prolonged durations, or repeated embedding update failures. For tracing, X-Ray can show call graphs and latency hot spots across external services. Cost telemetry estimates tokens per PR and flags outliers. Dashboards summarize P50/P95 review times and success rates.

## *Security: handling API keys and environment variables*

Secrets (OpenAI, GitHub, Pinecone) are injected as environment variables provided by AWS Secrets Manager or Parameter Store, with IAM roles granting decrypt/read at runtime. I never log secrets, and any debug logging redacts headers. The Lambda role follows least privilege, allowing only the S3 bucket, Pinecone endpoint, and required network egress. Build pipelines avoid writing secrets to images; they’re bound at deploy time. Local development uses .env but CI prevents committing it. If needed, keys are rotated automatically with Secrets Manager rotation.

## *Security: S3 access management*

The S3 bucket is private, encrypted at rest (SSE-S3 or KMS), and access is limited to the Lambda’s IAM role with resource-level policies. Objects are versioned to enable rollback and to support optimistic concurrency on updates. Server-side encryption and TLS in transit protect the chunk store. Bucket policies restrict public access and enforce TLS. Access logs can be enabled to audit reads/writes. If cross-account access were needed, I’d use bucket policies with condition keys and explicit principals.

## *Security: preventing code data leakage*

The service only fetches diffs and specific files for repos it’s configured to watch, and it never forwards code externally except to OpenAI for processing (documented and opt-in). Logs are scrubbed of code content; only metadata and small snippets (previews) appear, if at all. PR comments avoid reproducing large code blocks; they reference changed lines and explanations instead. I’d add data retention policies that expire temporary artifacts and logs. Network egress can be controlled via VPC endpoints and explicit allowed domains. If required, I could run with a self-hosted model or apply OpenAI’s data control options.

## *Scaling to thousands of concurrent PRs*

I’d decouple ingestion from processing with SQS: the webhook handler enqueues a job and returns immediately, and a fleet of worker Lambdas (or Fargate tasks) drains the queue with controlled concurrency. Per-worker concurrency is bounded by semaphores to respect OpenAI/Pinecone limits; autoscaling is driven by queue depth and age. Embedding updates are batched and parallelized, and a cache (e.g., Redis) stores frequent retrieval results to reduce query load. Provisioned concurrency smooths cold starts; Step Functions orchestrate multi-stage flows with retries and compensation. Budget controls estimate per-job token use and throttle or defer expensive jobs. This architecture scales horizontally while protecting dependencies.


## *Scaling Pinecone queries*

Batch queries per file or per PR where possible, and reuse query vectors for similar chunks. Apply strict metadata filters to keep top_k small and results precise; widen scope only when confidence is low. Warm up connections and use connection pooling to reduce per-call latency. Cache hot results keyed by (repo, path, hash) for short TTLs, since many PRs touch similar code. Monitor queries-per-second and P95 latency; raise limits or add replicas if needed. If costs rise, compress vectors or prune low-value chunks.

## *If the model slows or gets more expensive—optimizations*

Shift as much work as possible to retrieval and lightweight heuristics (e.g., classify diffs and only deep-review impactful files). Batch per-file reviews where prompts are small, and move summarization to a cheaper or distilled model. Add token-aware truncation and content ranking so only the most relevant context enters the prompt. Cache reviews for unchanged diffs across pushes to the same PR. Negotiate lower latency models or use “mini” variants for file reviews while reserving premium models for summarization. Profile prompts to remove verbosity and reduce token count.

## *Extending to automated code fixes*

I’d introduce a “fixer” agent that proposes patch hunks constrained to the diff scope, then validates them with syntax checks and lightweight static analysis. The system would open a suggested-commit PR or push to a feature branch with a checklist of changes. Guardrails would include tests (if present), formatting, and lints, plus a dry-run mode. Retrieval would include style guides and project conventions to fit the repo’s idioms. A human-in-the-loop flow would allow maintainers to accept, edit, or reject suggestions. Over time, feedback would tune prompts and heuristics.

## *Proudest part of the project*

I’m proud of the end-to-end orchestration that keeps latency low while providing meaningful, context-aware reviews. Splitting diffs by file and running parallel reviews delivers near-constant latency regardless of file count, and the RAG layer keeps feedback grounded in the repo. The architecture cleanly separates concerns: ingestion, retrieval, analysis, synthesis, and persistence. It’s also cost-aware—using a cheaper model for file analysis and a stronger model only for final synthesis. The system is pragmatic: it favors partial progress over perfection and degrades gracefully. For a compact codebase, it demonstrates a lot of real-world engineering trade-offs.

## *Hardest bug I fixed*

The trickiest issue was ensuring the correct version of files were embedded after updates; an early iteration mistakenly fetched from main rather than the PR head, causing drift between vectors and actual code. This manifested as inconsistent context and confusing reviews that referenced old code. The fix was to pull the head ref or commit SHA from the webhook payload and fetch content by SHA to avoid branch ambiguity. I added logging and assertions around ref resolution to catch regressions. It highlighted how subtle mismatches in data sources can cascade through retrieval to model outputs. It also pushed me to think about idempotency and versioning holistically.

## *If I had another month, what would I improve?*

I’d productionize reliability: queue-based orchestration, retries/backoff everywhere, and optimistic concurrency for the S3 store. I’d switch Python chunking to AST or tree-sitter for more accurate semantic units and expand language coverage. The embedding pipeline would be batched and parallel, with caching and scheduled rebuilds. I’d add robust observability—dashboards for latency, cost, retrieval quality, and review usefulness—and A/B tests for top_k and prompt variants. Adaptive throttling would protect against rate limits dynamically. Finally, I’d explore auto-fixes with patch proposals and validation, moving from reviewer to co-author.

## *What I learned about working with LLM APIs*

LLM systems reward careful scoping: focused prompts, small context, and tight instructions beat dumping everything into a giant prompt. Retrieval quality dominates output usefulness; a little precision in filters and chunking pays off more than model swapping. Latency and rate limits shape architecture—you need concurrency caps, batching, retries, and sometimes queues to stay robust. Deterministic IDs and idempotency are essential when multiple components (S3, Pinecone, GitHub) must remain consistent. Observability is non-negotiable; without timings and structured logs, you’re flying blind. Finally, designing for partial success and graceful degradation makes agentic systems feel dependable to end users.

### Notes:

I prepared way more than necessary. They asked decently basic questions, just a general walkthrough of the project end-to-end. I did well in explaining it as I went, and answered nearly all of their questions unknowingly through my in-depth explanations 