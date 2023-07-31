# Current Project: Enhancing WebSearchAgent

## Task Description
The goal of this project is to enhance the existing `WebSearchAgent` in the Marvin platform to classify a user query, search the web, scrape results, synthesize those results, compare them with the user query, and loop until an answer is found or the user stops the process.

## Task List
1. Extend the `WebSearchAgent` class in `cookbook/apps/web_search_agent.py` to create a custom agent.
2. Modify the `classify_query` method in the custom agent to suit specific classification requirements.
3. Modify the `search_web` method in the custom agent to suit specific web search requirements.
4. Modify the `parse_results` method in the custom agent to scrape and parse the search results as per specific needs.
5. Add a new method in the custom agent for synthesizing the parsed results into a coherent answer.
6. Add a new method in the custom agent for comparing the synthesized answer with the user query.
7. Modify the `respond_or_search_again` method in the custom agent to loop the search, scrape, synthesize, and compare process until an answer is found or the user stops the process.
8. Modify the `respond_or_search_again` method in the custom agent to respond to the user with the final answer in a user-friendly format.

## Cross-File Dependencies
- `cookbook/apps/web_search_agent.py`: This file contains the `WebSearchAgent` class that will be extended to create the custom agent.
- `cookbook/apps/agent.py`: This file contains the `Agent` class that the `WebSearchAgent` class inherits from. It may need to be referenced for understanding the base functionality.

## Progress Tracking
- [x] Task 1: Extend the `WebSearchAgent` class in `cookbook/apps/web_search_agent.py` to create a custom agent.
- [ ] Task 2: Modify the `classify_query` method in the custom agent to suit specific classification requirements.
- [ ] Task 3: Modify the `search_web` method in the custom agent to suit specific web search requirements.
- [ ] Task 4: Modify the `parse_results` method in the custom agent to scrape and parse the search results as per specific needs.
- [ ] Task 5: Add a new method in the custom agent for synthesizing the parsed results into a coherent answer.
- [ ] Task 6: Add a new method in the custom agent for comparing the synthesized answer with the user query.
- [ ] Task 7: Modify the `respond_or_search_again` method in the custom agent to loop the search, scrape, synthesize, and compare process until an answer is found or the user stops the process.
- [ ] Task 8: Modify the `respond_or_search_again` method in the custom agent to respond to the user with the final answer in a user-friendly format.

## Context
This `current_project.md` file was created to track the progress of the project and maintain context across multiple sessions with the GPT4-32k agent. The agent sometimes crashes and loses context, so this file will be used to reference and update the project status as work continues.
