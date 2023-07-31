# Current Project: Enhancing WebSearchAgent

## Task Description
The goal of this project is to enhance the existing `WebSearchAgent` in the Marvin platform to classify a user query, search the web, scrape results, synthesize those results, compare them with the user query, and loop until an answer is found or the user stops the process.

## Task List
1. Extend the `WebSearchAgent` class in `cookbook/apps/web_search_agent.py` to create a custom agent.
2. Modify the `classify_query` method in the custom agent to suit specific classification requirements.
3. Modify the `search_web` method in the custom agent to suit specific web search requirements.
    - Modify the `search_web` method to accept additional parameters that represent the live context.
    - Use the live context to determine the search requirements.
    - Modify the search query and parameters based on the determined search requirements.
    - Return the search results from the `DuckDuckGoSearch` tool.
4. Modify the `parse_results` method in the custom agent to scrape and parse the search results as per specific needs.
5. Add a new method in the custom agent for synthesizing the parsed results into a coherent answer.
6. Add a new method in the custom agent for comparing the synthesized answer with the user query.
7. Modify the `respond_or_search_again` method in the custom agent to loop the search, scrape, synthesize, and compare process until an answer is found or the user stops the process.
8. Modify the `respond_or_search_again` method in the custom agent to respond to the user with the final answer in a user-friendly format.

## Cross-File Dependencies
- `cookbook/apps/web_search_agent.py`: This file contains the `WebSearchAgent` class that will be extended to create the custom agent.
- `cookbook/apps/agent.py`: This file contains the `Agent` class that the `WebSearchAgent` class inherits from. It may need to be referenced for understanding the base functionality.
- `src/marvin/tools/github.py`: This file contains the `GitHubRepo` tool that can be used to search for up-to-date GitHub projects.
- `src/marvin/components/ai_model.py`: This file contains the `APIDoc` model that can be used to check API documentation before writing unique API calls.
- `cookbook/apps/documentation_agent.py`: This file contains the `DocumentationAgent` class that can be used to update documentation.
- `cookbook/apps/chatbot.py`: This file contains the `Chatbot` class that can be used to interact with the user.
- `action_based_spec.md`: This file contains the specifications for various AI tools that should be leveraged to power much of the logic in the `WebSearchAgent`.

## Note
When possible, the logic in the `WebSearchAgent` should be powered by the AI tools as defined in the `action_based_spec.md` file. This will ensure that the agent is leveraging the full capabilities of the Marvin platform.

## Progress Tracking
- [x] Task 1: Extend the `WebSearchAgent` class in `cookbook/apps/web_search_agent.py` to create a custom agent.
- [x] Task 2: Modify the `classify_query` method in the custom agent to suit specific classification requirements.
- [ ] Task 3: Modify the `search_web` method in the custom agent to suit specific web search requirements.
- [ ] Task 4: Modify the `parse_results` method in the custom agent to scrape and parse the search results as per specific needs.
- [ ] Task 5: Add a new method in the custom agent for synthesizing the parsed results into a coherent answer.
- [ ] Task 6: Add a new method in the custom agent for comparing the synthesized answer with the user query.
- [ ] Task 7: Modify the `respond_or_search_again` method in the custom agent to loop the search, scrape, synthesize, and compare process until an answer is found or the user stops the process.
- [ ] Task 8: Modify the `respond_or_search_again` method in the custom agent to respond to the user with the final answer in a user-friendly format.

## Context
This `current_project.md` file was created to track the progress of the project and maintain context across multiple sessions with the GPT4-32k agent. The agent sometimes crashes and loses context, so this file will be used to reference and update the project status as work continues.
