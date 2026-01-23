People to know
Ada Lovelace
Douglas Engelbart
Alan Kay

Key AI usage
LLM integration
Embeddings
Machine Learning

Mention:
Ai rag at pm accel
Ai rag at git lint
Lin and log regression with ml
Currently building a xgboost ml model for tennis match prediction, am feature engineering right now
Larger goal to start deep learning and transformers, and plan for my next project to use huggingface transformers to smart sort emails and categorize them automatically
MENTION: how i use ai llms in my day to day workflow and coding/creation



What is Notion AI?
Notion AI is a chatbot that is also a personal assistant. Powered by the most commonly used and best of the market LLMs, like Claude and ChatGPT, Notion AI helps answer questions and automate/fill in tasks. This can be in the form of filling in notes and documents with suggestions, fixing errors, creating boilerplate rough drafts for emails and such, analyzing files, and more. It has context from Notion workspaces that the user has, which provide better customizability and tailoring of responses to the user

RAG - more than likely has a rag component in the AI pipeline to retrieve relevant documents, pages, workspaces, etc (has integration with google drive and more)

Creates block of suggested improvements, which is then inserted into its react frontend, more than likely in a component that is created at time of prompting. Its then loaded into the webpage and saved, using Notion’s Block API


What skills do I have that align with their tech?
I have skills in implementing backend services, particularly in FastAPI, that integrate LLMs into the product, leveraging it to do many different things.



What experiences may I have that are useful/applicable to their product?
Primary - Professional:
I have experience at PM Accelerator building a FastAPI backend API that uses LLMs to improve resumes in relation to the Product Manger career industry. I did this, in particular, using ChatGPT 4o-mini as the prototype model, converting uploaded PDF format resumes to plain text and feeding it into the LLM as the input. I also implemented RAG where it would retrieve resumes gathered in a dataset that DID pass a specific role the user was targeting (like if the user was trying to pass resume ATS screening for Associate Product Manager), and using similarity vector search for description bullet points that are tagged with the user’s desired role. This allows for the bullet point to be compared against other bullet points that HAVE passed, and be changed to follow their format or use their keywords as well.
Uses Pinecone for embeddings of bullet points (small enough to be stored internally)
Uses MongoDB to store the user’s completed resume in text, which is then converted to PDF format upon download request
Worked with an AI engineer to implement LangChain with different models as well, like Llama, but did not complete before end of internship


Primary - Personal:
I have personal project experience in my project, Git-Lint. This project is an automated code reviewing agent system, using RAG and the OpenAI Agents SDK to analyze code diffs with codebase context, and summarize the change made, whether it can be improved syntactically or anything to follow coding conventions and such, and whether this has any significant impacts on the flow of the codebase (potentially causing runtime errors and such). It uses an orchestration agent, which manages the overall pipeline, passing off tasks to certain agents and functions to retrieve context, review chunks, update storage for new changes, and post comments. I embedded individual functions from files in each repository, that way any changes in a diff would be in the prompt along with its accompanying function and any functions that may be used in relation.
Deployed on AWS Lambda using FastAPI for lightweight building, it is asynchronous by design, and decreases idle costs
Embeddings stored in Pinecone, entire content stored in cloud storage
Used AWS S3 to store functions with hashes to their embeddings in Pinecone

	I also have experience in my current machine learning project, MatchPointAI, where I am creating an XGBoost prediction model to predict outcomes of matchups between professionally ranked tennis players. I just completed my feature engineering and am in the process of creating my training and test set splits to enter the training phase. So far, for the dataset, I have gathered data from 1968-2024, across 389,000 rows, reaching a total of slightly over 1200 players with enough match history to be accurate. I implemented 5-KNN imputation to fill in missing values, searching for similar players in the same rank and approximate era to ensure logical and accurate imputation of missing player statistics.
Tech used: Pandas, NumPy, Scikit-learn
 

In 3-4 sentences, describe myself.
My name is Kyle, an upcoming junior studying Computer Science at the University of California, San Diego. I was an intern previously at PM Accelerator and Trace, where I performed full-stack development and quality assurance scripting. I’m currently interning at ForOurLastNames, a fintech company that is working in gamifying the wealth-building experience. I am in charge of the AWS hosting for the initial launch, as well as creating and integrating a custom LangChain chatbot for user experience and ease of usage of the app. My current skillset is centered around full-stack and backend development, and I have a large interest in AI and machine learning, and am teaching myself machine learning in both theory and application. I hope one day to enter the workforce as a software engineer, specializing in AI and ML applications, and contribute to the progressive advancement of technology.

What is my biggest strength?
My biggest strength is that I am relentlessly curious and quick at picking up new skills. Whenever I find a heavy interest in building something, I tend to work really hard at it, learning everything I can surrounding the project, and building clean, manageable, and scalable applications. I spend a large majority of my time outside of school and other obligations engaging in self-learning, teaching myself new technologies and deepening my understanding on systems so that future projects that I build will be of far better standards. As such, I have become very adept at learning on my own, and very quickly at that.

What is my biggest weakness?
My biggest weakness is that I need to seek help and rely on others sooner. Given my nature, I tend to dive very deeply into problems and tasks, which has helped me grow my foundational and technical skills well. I have realized that, at times, this is detrimental, since the excess time I spend trying to figure out a problem or solve something alone could slow down the team’s overall production progress. I am trying to be more proactive about when to take a step back and get others’ opinions and contributions, which would lead to faster and possibly better outcomes.

What is my motivation behind taking this career path?
My motivation behind wanting to become a software engineer is that I have always had an interest in building things. As a child, I played with Legos a lot, sometimes following the instructions, and other times, utilizing any and every piece to be creative and build my very own toys. Later on, I found an interest in computer hardware, becoming obsessed with PC parts and building computers, which then transferred to building keyboards as well. I’ve built both my own PC and keyboard with the information I've gathered through my interests. Then, I discovered coding through my AP Computer Science A class in my senior year of high school. I really fell in love with the concept of being able to build anything you could ever want, by writing a series of words and commands to a computer, that could have affects that would revolutionize the world, like the invention of the search engine, of platforms like Amazon, or even transformers like ChatGPT. I thrived in that environment, reaching the top of my class. More so, I had finally found something that resonated with me. Throughout middle and high school, I really struggled with who I was and what I was meant to be, and had many, many internal conflicts about this. At times, I felt hopeless and lost, stressing about the path I was going to take, where I didn’t even how or where I would take my next step. When I decided to pursue software engineering, it felt like I finally had solid ground beneath my feet, and that when I looked into my future, instead of seeing nothing, I had a vision and a path to follow. Anything less than pursuing this dream would feel like I would be betraying myself, which is what motivates me to work harder than anything that could get in my way, and become the greatest software engineer I could be.

What are my interests within the industry?
I have heavy interests in full-stack development, especially the backend development aspect. I really appreciate the complexity behind creating intricate systems to be implemented in various applications, and being able to not only produce the server portion, but t have full control over the database used, the process of continual development, and being able to design my frontend to fit my needs (I am not the most visually creative, however). I also really enjoy learning about machine learning. Especially with transformers,  I think it is fascinating how we can use mathematically trained models on certain datasets, that can make such accurate and elaborate predictions. I hope to see them become even more advanced and capable in the future. 


Custom Sales Pitch - Selling Myself
I’m Kyle, and I’m a rising junior majoring in Computer Science, and will be transferring this fall to UCSD, and I’ve had two previous software engineering internships and a current one. My most recent professional experience was in a role where I focused on applying AI in practical settings, and the other was in a testing/debugging role for automation testing scripts in Python. I have also worked on projects revolving around AI and am very interested in the world of software engineering and being able to integrate AI and machine learning into everything I build. 


Screening notes:
In office mon tues thurs, remote/your choice wed fri
