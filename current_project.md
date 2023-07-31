# Current Project: Enhancing WebSearchAgent
## Task List
1. Extend the `WebSearchAgent` class in `cookbook/apps/web_search_agent.py` to create a custom agent.
    - Created a new class `CustomWebSearchAgent` that extends `WebSearchAgent`.
    - Initialized the new class with the same parameters as `WebSearchAgent`.
    - TODO: Implement the following methods in the `WebSearchAgent` class:
        - `classify_query(self, query)`: Classify the user's query into predefined categories using the QueryType classifier.
        - `determine_search_requirements(self, live_context = {})`: Determine the search requirements based on the live context.
        - `modify_search_requirements(self, query, search_requirements)`: Modify the query and parameters based on the search requirements.
        - `search_web(self, query, live_context = {})`: Search the web based on the user's query and the live context using the DuckDuckGoSearch tool.
        - `extract_results(self, search_results)`: Extract the search results from the raw search results using ScrapeGhost and the DuckDuckGoSearch tool.
        - `parse_results(self, results)`: Parse the search results.
        - `evaluate_results(self, parsed_results, query)`: Evaluate the relevance of the parsed results in reference to the user query.
        - `respond_or_search_again(self, evaluated_results)`: Respond to the user's query or continue the search based on the evaluated results.
2. Modify the `classify_query` method in the custom agent to suit specific classification requirements.
    - Partially updated the `classify_query` method to use the `QueryType` classifier.
    - The classifier is expected to categorize queries into types such as FACTUAL_INFORMATION, LATEST_NEWS, GITHUB_PROJECT, API_DOCUMENTATION, DEBUGGING_HELP, etc.
    - TODO: Implement the logic to classify the query using the `QueryType` classifier.
3. Modify the `search_web` method in the custom agent to suit specific web search requirements.
    - Modify the `search_web` method to accept additional parameters that represent the live context.
    - Use the live context to determine the search requirements.
    - Modify the search query and parameters based on the determined search requirements.
    - Use the `DuckDuckGoSearch` tool to search the web with the modified query and parameters.
    - Return the search results.
    - TODO: Implement the `determine_search_requirements` and `modify_search_requirements` methods to process the `live_context` and generate a relevant web query.
    - TODO: Check and leverage the `action_based_spec.md` for Marvin commands.
4. Modify the `parse_results` method in the custom agent to scrape and parse the search results as per specific needs.
    - TODO: Implement the `parse_results` method to parse the search results using the `GitHubRepo` and `APIDoc` models.
5. Add a new method in the custom agent for synthesizing the parsed results into a coherent answer.
    - TODO: Implement this method to synthesize the parsed results into a coherent answer.
6. Add a new method in the custom agent for comparing the synthesized answer with the user query.
    - TODO: Implement this method to compare the synthesized answer with the user query.
7. Modify the `respond_or_search_again` method in the custom agent to loop the search, scrape, synthesize, and compare process until an answer is found or the user stops the process.
    - TODO: Implement this method to loop the search, scrape, synthesize, and compare process until an answer is found or the user stops the process.
8. Modify the `respond_or_search_again` method in the custom agent to respond to the user with the final answer in a user-friendly format.
    - TODO: Implement this method to respond to the user with the final answer in a user-friendly format.

## Progress Tracking
- [x] Task 1: Extend the `WebSearchAgent` class in `cookbook/apps/web_search_agent.py` to create a custom agent.
- [ ] Task 2: Modify the `classify_query` method in the custom agent to suit specific classification requirements. (Incomplete, subtasks pending)
- [ ] Task 3: Modify the `search_web` method in the custom agent to suit specific web search requirements. (Incomplete, subtasks pending)
- [ ] Task 4: Modify the `parse_results` method in the custom agent to scrape and parse the search results as per specific needs.
- [ ] Task 5: Add a new method in the custom agent for synthesizing the parsed results into a coherent answer.
- [ ] Task 6: Add a new method in the custom agent for comparing the synthesized answer with the user query.
- [ ] Task 7: Modify the `respond_or_search_again` method in the custom agent to loop the search, scrape, synthesize, and compare process until an answer is found or the user stops the process.
- [ ] Task 8: Modify the `respond_or_search_again` method in the custom agent to respond to the user with the final answer in a user-friendly format.

## API Spec Snippets

### AI Classifier Spec
`ai_classifier` is implemented as a Python decorator that adds additional attributes and methods to an Enum class.

```python
from src.marvin.components.ai_classifier import ai_classifier

@ai_classifier
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

# Classify text
color = Color("I like the color of the sky.")
print(color)  # Color.BLUE
```

### AIFunction Spec
`AIFunction` is a class that represents a Python function with a signature and docstring as a prompt for an AI to predict the function's output.

```python
from src.marvin.components.ai_function import ai_fn

@ai_fn
def add(a: int, b: int) -> int:
    """Adds two integers."""

# Predict function output
result = add(1, 2)
print(result)  # 3
```

### ScrapeGhost Spec
ScrapeGhost is a tool for extracting structured data from web pages using GPT-3. It takes a schema that describes the shape of the data you wish to extract, and returns a dictionary of that shape.

```python
from scrapeghost import SchemaScraper, CSS

schema = {"name": "str", "committees": [], "bio": "str"}
scraper = SchemaScraper(schema)
result = scraper.scrape("https://norton.house.gov/about/full-biography")
print(result.data)
```
## Cross-File Dependencies
- `cookbook/apps/web_search_agent.py`: This file contains the `WebSearchAgent` class that will be extended to create the custom agent. The `search_web` method in this class uses a context dictionary to maintain the state of the conversation or task. This dictionary could include the chat log/history, the specific question/problem identified by the classifier, or any other relevant information.
- `cookbook/apps/agent.py`: This file contains the `Agent` class that the `WebSearchAgent` class inherits from. It may need to be referenced for understanding the base functionality. The `AIApplication` component in this class could be used to maintain the state of the conversation or task, which could then be passed to the `search_web` method as the context.
- `src/marvin/tools/github.py`: This file contains the `GitHubRepo` tool that can be used to search for up-to-date GitHub projects. This tool could be used in the `search_web` method to search for GitHub projects related to the user's query.
- `src/marvin/components/ai_model.py`: This file contains the `APIDoc` model that can be used to check API documentation before writing unique API calls. The `AIModel` component in this class could be used to parse the search results into structured data.
- `cookbook/apps/documentation_agent.py`: This file contains the `DocumentationAgent` class that can be used to update documentation. This class could be used to update the documentation of the `WebSearchAgent` class as changes are made.
- `cookbook/apps/chatbot.py`: This file contains the `Chatbot` class that can be used to interact with the user. This class could be used to communicate the search results to the user in a user-friendly format.
- `action_based_spec.md`: This file contains the specifications for various AI tools that should be leveraged to power much of the logic in the `WebSearchAgent`. These tools include the `AIEnum` component for classifying the user's query and the `AIModel` component for parsing the search results.

## Note
When possible, the logic in the `WebSearchAgent` should be powered by the AI tools as defined in the `action_based_spec.md` file. This will ensure that the agent is leveraging the full capabilities of the Marvin platform. Always check the `action_based_spec.md` for Marvin commands to ensure we're leveraging them as well as possible.

When proposing code changes, ensure that the "below the line" section of an edit block contains the updated code, not just the new additions. If the existing code is not included, it would be removed. This is particularly important when working with large blocks of code or entire classes.

## Progress Tracking
- [x] Task 1: Extend the `WebSearchAgent` class in `cookbook/apps/web_search_agent.py` to create a custom agent.
- [ ] Task 2: Modify the `classify_query` method in the custom agent to suit specific classification requirements. (Incomplete, subtasks pending)
- [ ] Task 3: Modify the `search_web` method in the custom agent to suit specific web search requirements. (Incomplete, subtasks pending)
- [ ] Task 4: Modify the `parse_results` method in the custom agent to scrape and parse the search results as per specific needs.
- [ ] Task 5: Add a new method in the custom agent for synthesizing the parsed results into a coherent answer.
- [ ] Task 6: Add a new method in the custom agent for comparing the synthesized answer with the user query.
- [ ] Task 7: Modify the `respond_or_search_again` method in the custom agent to loop the search, scrape, synthesize, and compare process until an answer is found or the user stops the process.
- [ ] Task 8: Modify the `respond_or_search_again` method in the custom agent to respond to the user with the final answer in a user-friendly format.

## Context
This `current_project.md` file was created to track the progress of the project and maintain context across multiple sessions with the GPT4-32k agent. The agent sometimes crashes and loses context, so this file will be used to reference and update the project status as work continues.
