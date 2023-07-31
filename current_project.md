# Current Project: Enhancing WebSearchAgent
The goal of this project is to enhance the `WebSearchAgent` class in `cookbook/apps/web_search_agent.py` to create a more robust and intelligent web search agent. The enhanced `WebSearchAgent` will be capable of classifying user queries, determining search requirements, modifying search requirements, searching the web, extracting and parsing search results, synthesizing parsed results into a coherent answer, comparing the synthesized answer with the user query, and responding to the user or continuing the search based on the evaluated results. The `WebSearchAgent` will leverage various AI tools and components from the Marvin platform to achieve these tasks.

## Project Context and Goals
The `WebSearchAgent` module is designed to be imported into other projects, specifically in the logic chain of conversational software development supporting chatbots. When called with the conversation history and the most recent message (the user's query to the chatbot), it will determine whether the question can be answered more robustly using information pulled from the web.

The module should also be capable of monitoring both the user's inputs and the chatbot's outputs. If a user request in a conversational flow can be enriched with web knowledge, the module will initiate a process of searching the web, collecting URLs, scraping those URLs, extracting information, distilling that information, checking its relevance, and if applicable, providing the chatbot with a rich, web-data-empowered response.

If the module fails to find relevant information, it will self-assess and determine whether it failed due to a bad search query/bad found data, or if it failed because the 'problem-solving' data doesn't exist. In the former case, it will requery with a reformulated query, alerting the calling program so it knows to alert the user. If it fails because there is no relevant data on the web, it will simply pass that information on to the calling program.

When plugged into the chatbot's side of the conversation, the module will process the response offered by the chatbot before it is presented to the user, validate that the answer makes sense given the conversation context and the web data, and where needed/relevant, provide the calling chatbot with an edited reply to proffer, or it will green-light the reply from the chatbot as 'good; web validated' or 'good; no web validation needed'.

The module is designed to be very portable, able to be plugged into a variety of contexts, using the dynamic structures offered by the Marvin `components` to manage black-boxed, unknown situations at runtime, and using tools like the `scrapeghost` API to extract web content from sites, given un-pre-defined contexts. To write things like the scrapeghost target schema, it will leverage Marvin components, as defined in the `action_based_spec.md`.

## Task List
1. Implement the `classify_query` method in the `WebSearchAgent` class to classify the user's query into predefined categories using the QueryType classifier. The classification of the query influences the subsequent steps of determining search requirements, modifying search requirements, and searching the web. The classification is done using the QueryType classifier, which is an AI classifier that classifies queries into predefined categories.
2. Implement the `determine_search_requirements` method in the `WebSearchAgent` class to determine the search requirements based on the live context. The live context, which contains the chat log/history and the specific question/problem identified by the classifier, is used to determine the search requirements. The search requirements are determined using the AIApplication tool, which maintains the state of the conversation or task.
3. Implement the `modify_search_requirements` method in the `WebSearchAgent` class to modify the query and parameters based on the search requirements. The query and search requirements are modified based on the search requirements determined in the previous step. The modification is done using the AIFunction tool, which predicts the function's output based on its signature and docstring.
4. Modify the `search_web` method in the `WebSearchAgent` class to search the web based on the user's query and the live context. The web search is conducted based on the user's query and the live context. The web search is done using the DuckDuckGoSearch tool, and the search results are then extracted and parsed for relevance to the user's query.
5. Implement the `extract_results` method in the `WebSearchAgent` class to extract the search results from the raw search results using the ScrapeGhost API. The search results are extracted from the raw search results using the ScrapeGhost API. The extracted results are then parsed and evaluated for relevance to the user's query, and the agent responds to the user's query or continues the search based on the evaluated results.
6. Implement the `parse_results` method in the `WebSearchAgent` class to parse the search results using the ScrapeGhost API and the AIFunction or AIApplication tools as is relevant.
7. Implement the `evaluate_results` method in the `WebSearchAgent` class to evaluate the relevance of the parsed results in reference to the user query using the AIFunction tool.
8. Implement the `respond_or_search_again` method in the `WebSearchAgent` class to respond to the user's query or continue the search based on the evaluated results using the AIApplication tool.

## Progress Tracking
- [x] Task 1: Implement the `classify_query` method in the `WebSearchAgent` class.
- [x] Task 2: Implement the `determine_search_requirements` method in the `WebSearchAgent` class.
- [x] Task 3: Implement the `modify_search_requirements` method in the `WebSearchAgent` class.
- [x] Task 4: Modify the `search_web` method in the `WebSearchAgent` class.
- [x] Task 5: Implement the `extract_results` method in the `WebSearchAgent` class.
- [x] Task 6: Implement the `parse_results` method in the `WebSearchAgent` class.
- [x] Task 7: Implement the `evaluate_results` method in the `WebSearchAgent` class.
- [x] Task 8: Implement the `respond_or_search_again` method in the `WebSearchAgent` class.
- [x] Task 9: Modify the `determine_search_requirements` and `respond_or_search_again` methods in the `WebSearchAgent` class to use the shared `AIApplication` instance (`self.ai_application`) instead of creating new instances.
- [x] Task 10: Add a definition for the `evaluate_relevance` method in the `WebSearchAgent` class.
- [x] Task 11: Enhance the docstrings for the `parse_results`, `evaluate_results`, and `respond_or_search_again` methods in the `WebSearchAgent` class to provide more detailed information.
- [x] Task 12: Add usage instructions for the `WebSearchAgent` module at the top of the `cookbook/apps/web_search_agent.py` file.

## API Spec Snippets
(No changes needed)

## Cross-File Dependencies
(No changes needed)

## Note
When possible, the logic in the `WebSearchAgent` should be powered by the AI tools as defined in the `action_based_spec.md` file. This will ensure that the agent is leveraging the full capabilities of the Marvin platform. Always check the `action_based_spec.md` for Marvin commands to ensure we're leveraging them as well as possible.

When proposing code changes, ensure that the "below the line" section of an edit block contains the updated code, not just the new additions. If the existing code is not included, it would be removed. This is particularly important when working with large blocks of code or entire classes.

## Proposed Changes
1. Modify the `determine_search_requirements` and `respond_or_search_again` methods in the `WebSearchAgent` class to use the shared `AIApplication` instance (`self.ai_application`) instead of creating new instances.
2. Add a definition for the `evaluate_relevance` method in the `WebSearchAgent` class.
3. Enhance the docstrings for the `parse_results`, `evaluate_results`, and `respond_or_search_again` methods in the `WebSearchAgent` class to provide more detailed information.
4. Add usage instructions for the `WebSearchAgent` module at the top of the `cookbook/apps/web_search_agent.py` file.

## Context
This `current_project.md` file was created to track the progress of the project and maintain context across multiple sessions with the GPT4-32k agent. The agent sometimes crashes and loses context, so this file will be used to reference and update the project status as work continues.

As a reminder, top level goals of this project are:
The WebSearchAgent class has several methods that need to be implemented:

1. `classify_query(self, query)`: This method should classify the user's query into predefined categories using the QueryType classifier. We can use the AIClassifier tool from Marvin to implement this.
2. `determine_search_requirements(self, live_context = {})`: This method should determine the search requirements based on the live context. We can use the AIApplication tool from Marvin to maintain the state of the conversation or task, which can then be used to determine the search requirements.
3. `modify_search_requirements(self, query, search_requirements)`: This method should modify the query and parameters based on the search requirements. We can use the AIFunction tool from Marvin to predict the function's output based on its signature and docstring.
4. `search_web(self, query, live_context = {})`: This method should search the web based on the user's query and the live context using the DuckDuckGoSearch tool. We can use the DuckDuckGoSearch tool directly as it is.
5. `extract_results(self, search_results)`: This method should extract the search results from the raw search results using ScrapeGhost and the DuckDuckGoSearch tool. We can use the ScrapeGhost tool to extract structured data from the search results.
6. `parse_results(self, results)`: This method should parse the search results. We can use the AIModel tool from Marvin to parse the search results into structured data.
7. `evaluate_results(self, parsed_results, query)`: This method should evaluate the relevance of the parsed results in reference to the user query. We can use the AIFunction tool from Marvin to predict the function's output based on its signature and docstring.
8. `respond_or_search_again(self, evaluated_results)`: This method should respond to the user's query or continue the search based on the evaluated results. We can use the AIApplication tool from Marvin to maintain the state of the conversation or task, which can then be used to decide whether to respond or search again.

We should refer to ahd this current_project.md file before and after each session to track progress and context.  As tasks are updated, edited, and completed, we should update this tracking file accordingly.  If we find that a task is already completed when we set out to solve it (if instructed by the tracking system here), that is great news.  We can immediately check off the task and move on to the next.  We should just be robust in verifying that all parts of a task are implemented, adhering strictly to all nuance and detai.

After completing a task, we should review that task (without proposing edit blocks; just review) to ensure it meets requirements and quality standards. If it does, we can then mark that task as complete in the progress tracking section above. If it does not meet requirements, we should revisit that task and propose improvements.