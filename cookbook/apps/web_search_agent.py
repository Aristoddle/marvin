"""
The `WebSearchAgent` class is designed to enhance the capabilities of a chatbot 
by leveraging web search. It has several methods that need to be implemented:

1. `classify_query(self, query)`: This method should classify the user's query 
into predefined categories using the QueryType classifier. We can use the 
AIClassifier tool from Marvin to implement this.

2. `determine_search_requirements(self, live_context = {})`: This method should 
determine the search requirements based on the live context. We can use the 
AIApplication tool from Marvin to maintain the state of the conversation or task, 
which can then be used to determine the search requirements.

3. `modify_search_requirements(self, query, search_requirements)`: This method 
should modify the query and parameters based on the search requirements. We can 
use the AIFunction tool from Marvin to predict the function's output based on 
its signature and docstring.

4. `search_web(self, query, live_context = {})`: This method should search the 
web based on the user's query and the live context using the DuckDuckGoSearch tool. 
We can use the DuckDuckGoSearch tool directly as it is.

5. `extract_results(self, search_results)`: This method should extract the search 
results from the raw search results using ScrapeGhost and the DuckDuckGoSearch tool. 
We can use the ScrapeGhost tool to extract structured data from the search results.

6. `parse_results(self, results)`: This method should parse the search results. 
We can use the AIModel tool from Marvin to parse the search results into structured data.

7. `evaluate_results(self, parsed_results, query)`: This method should evaluate 
the relevance of the parsed results in reference to the user query. We can use 
the AIFunction tool from Marvin to predict the function's output based on its 
signature and docstring.

8. `respond_or_search_again(self, evaluated_results)`: This method should respond 
to the user's query or continue the search based on the evaluated results. We can 
use the AIApplication tool from Marvin to maintain the state of the conversation 
or task, which can then be used to decide whether to respond or search again.

Here's an example of how to use the `WebSearchAgent` class:

```python
from cookbook.apps.web_search_agent import WebSearchAgent

# Create an instance of the WebSearchAgent class
web_search_agent = WebSearchAgent()

# Classify a user's query
query = "What's the weather like today?"
query_type = web_search_agent.classify_query(query)

# Determine the search requirements based on the live context
live_context = {"chat_log": ["What's the weather like today?", "It's sunny and warm."], 
                "question": "What's the weather like today?"}
search_requirements = web_search_agent.determine_search_requirements(live_context)

# Modify the query and parameters based on the search requirements
modified_query, parameters = web_search_agent.modify_search_requirements(query, 
                                                                    search_requirements)

# Search the web based on the user's query and the live context
search_results = web_search_agent.search_web(modified_query, live_context)

# Extract the search results from the raw search results
extracted_results = web_search_agent.extract_results(search_results)

# Parse the search results
parsed_results = web_search_agent.parse_results(extracted_results)

# Evaluate the relevance of the parsed results in reference to the user query
evaluated_results = web_search_agent.evaluate_results(parsed_results, query)

# Respond to the user's query or continue the search based on the evaluated results
response = web_search_agent.respond_or_search_again(evaluated_results, query, live_context)
```
"""

from marvin.tools.web import DuckDuckGoSearch
from marvin.components.ai_classifier import ai_classifier
from marvin.components.ai_application import AIApplication
from marvin.components.ai_function import AIFunction
from marvin.components.ai_model import AIModel
from marvin.components.ai_model_factory import AIModelFactory

from scrapeghost import SchemaScraper
from enum import Enum

import openai

openai.api_key = "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"


@ai_classifier
class QueryType(Enum):
    FACTUAL_INFORMATION = 1
    LATEST_NEWS = 2
    GITHUB_PROJECT = 3
    API_DOCUMENTATION = 4
    DEBUGGING_HELP = 5


class WebSearchAgent:
    description: str = "A custom web search agent"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.search_tool = DuckDuckGoSearch()
        self.ai_application = AIApplication(
            name="WebSearchAgent", description=self.description
        )

    def _format_response(self, evaluated_results: list) -> str:
        """
        Formats the search results into a human-readable string.

        Args:
            results (list): The search results to format.

        Returns:
            str: The formatted search results.
        """
        formatted_results = "\n".join(
            [f"Result: {result[0]}, Relevance Score: {result[1]}" for result in results]
        )
        return formatted_results

    def _evaluate_relevance(self, results: list, query: str) -> list:
        """
        Evaluates the relevance of the search results in reference to the user query.

        Args:
            results (list): The search results to evaluate.
            query (str): The user's query.

        Returns:
            list: The evaluated search results.
        """
        evaluated_results = []
        for result in results:
            # Construct a prompt for GPT-4
            prompt = (
                f"Given the query '{query}' and the search result '{result}', rate the"
                " relevance on a scale of 1 to 10."
            )

            # Use GPT-4 or GPT-4-32k based on the length of the prompt
            engine_name = "gpt-4" if len(prompt.split()) <= 5000 else "gpt-4-32k"

            # Use the selected engine to generate a relevance score
            response = openai.Completion.create(
                engine=engine_name, prompt=prompt, max_tokens=3
            )
            score = float(response.choices[0].text.strip())

            # Append the result and its score to the evaluated results
            evaluated_results.append((result, score))

        # Sort the results by their scores in descending order
        evaluated_results.sort(key=lambda x: x[1], reverse=True)

        return evaluated_results

    def classify_query(self, query):
        """
        Classify the user's query into predefined categories using the QueryType classifier.
        The classification of the query influences the subsequent steps of determining search
        requirements, modifying search requirements, and searching the web.
        """
        # Use the QueryType classifier to classify the user's query
        query_type = QueryType(query)

        # Return the classified query type
        return query_type

    async def determine_search_requirements(self, live_context=None):
        """
        Determine the search requirements based on the live context. The live context, which
        contains the chat log/history and the specific question/problem identified by the classifier,
        is used to determine the search requirements. The search requirements are determined using
        the AIApplication tool, which maintains the state of the conversation or task.

        Args:
            live_context (dict): The live context containing the chat log/history and the specific question/problem identified by the classifier.

        Returns:
            dict: The search requirements.
        """
        if live_context is None:
            live_context = {}

        search_requirements = await self.ai_application.run(live_context)
        return search_requirements

    def modify_search_requirements(self, query, search_requirements):
        """
        Modify the query and parameters based on the search requirements. The query and search
        requirements are modified based on the search requirements determined in the previous step.
        The modification is done using the AIFunction tool, which predicts the function's output
        based on its signature and docstring.

        Args:
            query (str): The user's query.
            search_requirements (dict): The search requirements.

        Returns:
            tuple: The modified query and parameters.
        """
        # Create an instance of AIFunction with the function being this method itself
        ai_function = AIFunction(fn=self.modify_search_requirements)

        # Use the AIFunction instance to predict the function's output based on the query and search requirements
        results = ai_function(query, search_requirements)
        modified_query = results[0] if len(results) > 0 else None
        parameters = results[1] if len(results) > 1 else None

        return modified_query, parameters

    async def search_web(self, query, live_context):
        """
        Search the web based on the user's query and the live context. The web search is conducted
        based on the user's query and the live context. The web search is done using the DuckDuckGoSearch
        tool, and the search results are then extracted and parsed for relevance to the user's query.

        The live context is a dictionary that contains information about the current state of the conversation or task.
        This could include the chat log/history, the specific question/problem identified by the classifier, or any other relevant information.

        This method uses the live context to determine the search requirements, modifies the query and parameters based on these requirements,
        and then uses the DuckDuckGoSearch tool to search the web with the modified query and parameters.

        Args:
            query (str): The user's query.
            live_context (dict): The live context containing the chat log/history and the specific question/problem identified by the classifier.

        Returns:
            str: The search results.
        """
        # Determine the search requirements based on the live context
        search_requirements = await self.determine_search_requirements(live_context)

        # Modify the query and parameters based on the search requirements
        modified_query, _ = self.modify_search_requirements(
            query, search_requirements
        )

        # Search the web using the DuckDuckGoSearch tool with the modified query and parameters
        search_results = self.search_tool.run(modified_query)

        return search_results

    async def extract_results(self, search_results):
        """
        Extract the search results from the raw search results using the ScrapeGhost API. The search
        results are extracted from the raw search results using the ScrapeGhost API. The extracted
        results are then parsed and evaluated for relevance to the user's query, and the agent responds
        to the user's query or continues the search based on the evaluated results.

        Args:
            search_results (str): The search results.

        Returns:
            str: The extracted search results, getting website URLs from DDG, and using ScrapeGhost to pull their data.
        """

    
        # Use the AIApplication instance to dynamically determine the structure of the data
        schema = await self.ai_application.run(search_results)

        # Create an instance of the SchemaScraper class with the schema
        scraper = SchemaScraper(schema)

        # Scrape the raw search results
        scraped_data = scraper.scrape(search_results)

        # Convert the scraped data into an instance of an AI model
        extracted_results = AIModelFactory(scraped_data)


        return extracted_results

    def parse_results(self, results):
        """
        Further refine and personalize the search results using the AIModel tool from Marvin.

        This method takes the search results, which are already in a structured format provided by the ScrapeGhost API,
        and further refines and personalizes them. The goal is to extract the most salient data points, structure the data
        for easier management, and provide an opportunity for additional post-processing models, scripts, heuristics, and
        functions to further refine the data before passing it forward.

        The parsing and refining is done using the AIModel tool from Marvin, which is capable of parsing a wide variety of
        data types and structures, and can be customized to provide additional refinement and personalization.

        Args:
            results (list): The search results in a structured format provided by the ScrapeGhost API.

        Returns:
            list: The search results parsed and refined into a more personalized and manageable format.
        """
        parsed_results = AIModel.extract(results)
        return parsed_results

    def evaluate_results(self, parsed_results, query):
        """
        Evaluate the relevance of the parsed results in reference to the user query using the AIFunction tool.

        This method takes the parsed results and the user's query, and evaluates the relevance of each result
        in reference to the query. The evaluation is done using the AIFunction tool from Marvin, which predicts
        the function's output based on its signature and docstring.

        The goal is to determine how relevant each result is to the user's query, which can then be used to
        decide whether to respond to the user's query or continue the search.

        Args:
            parsed_results (list): The parsed search results.
            query (str): The user's query.

        Returns:
            list: The evaluated results, each with a relevance score.
        """
        # Define an AIFunction that evaluates the relevance of a result
        evaluate_relevance = AIFunction(fn=self._evaluate_relevance)

        # Use the AIFunction to evaluate the relevance of each result
        evaluated_results = [
            evaluate_relevance.run(result, query) for result in parsed_results
        ]

        return evaluated_results

    async def respond_or_search_again(self, evaluated_results, query, live_context):
        """
        Respond to the user's query or continue the search based on the evaluated results using the AIApplication tool.

        This method takes the evaluated results, the user's query, and the live context, and decides whether to respond
        to the user's query or continue the search. The decision is made using the AIApplication tool from Marvin, which
        maintains the state of the conversation or task.

        If the decision is to respond, the method formats the response and returns it. If the decision is to continue
        the search, the method conducts a new web search using the user's query and the live context, and returns the
        search results.

        Args:
            evaluated_results (list): The evaluated search results.
            query (str): The user's query.
            live_context (dict): The live context containing the chat log/history and the specific question/problem identified by the classifier.

        Returns:
            str: The response to the user's query or the new search results.
        """
        # Create an AIApplication that maintains the state of the conversation or task
        app = AIApplication(name="WebSearchAgent", description="A web search agent")

        # Use the AIApplication to decide whether to respond or search again
        decision = await app.run(evaluated_results)

        if decision == "respond":
            # If the decision is to respond, format the response
            response = AIFunction(fn=self._format_response(evaluated_results))
        else:
            # Otherwise, continue the search
            response = await self.search_web(query, live_context)

        return response


__all__ = ["WebSearchAgent"]
