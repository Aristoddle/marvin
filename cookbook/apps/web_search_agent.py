
from marvin.tools.web import DuckDuckGoSearch
from src.marvin.components.ai_classifier import ai_classifier
from src.marvin.components.ai_application import AIApplication
from src.marvin.components.ai_function import AIFunction
from src.marvin.components.ai_model import AIModel

from enum import Enum

import openai

openai.api_key = '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'

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

    def classify_query(self, query):
        """
        Classify the user's query into predefined categories using the QueryType classifier.
        """
        # Use the QueryType classifier to classify the user's query
        query_type = QueryType(query)

        # Return the classified query type
        return query_type

    def determine_search_requirements(self, live_context=None):
        """
        Determine the search requirements based on the live context.

        Args:
            live_context (dict): The live context containing the chat log/history and the specific question/problem identified by the classifier.

        Returns:
            dict: The search requirements.
        """
        if live_context is None:
            live_context = {}

        # Create an instance of the AIApplication tool
        app = AIApplication(name="WebSearchAgent", description="A web search agent")

        # Use the AIApplication instance to determine the search requirements based on the live context
        search_requirements = app.run(live_context)

        return search_requirements

    def modify_search_requirements(self, query, search_requirements):
        """
        Modify the query and parameters based on the search requirements.

        Args:
            query (str): The user's query.
            search_requirements (dict): The search requirements.

        Returns:
            tuple: The modified query and parameters.
        """
        # Create an instance of AIFunction with the function being this method itself
        ai_function = AIFunction(fn=self.modify_search_requirements)

        # Use the AIFunction instance to predict the function's output based on the query and search requirements
        modified_query, parameters = ai_function(query, search_requirements)

        return modified_query, parameters
    
    def search_web(self, query, live_context):
        """
        Search the web based on the user's query and the live context.

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
        search_requirements = self.determine_search_requirements(live_context)
        
        # Modify the query and parameters based on the search requirements
        modified_query, parameters = self.modify_search_requirements(query, search_requirements)

        # Search the web using the DuckDuckGoSearch tool with the modified query and parameters
        search_results = self.search_tool.run(modified_query)
        
        return search_results


    def extract_results(self, search_results):
        """
        Extract the search results from the raw search results using ScrapeGhost and the DuckDuckGoSearch tool.

        Args:
            search_results (str): The search results.

        Returns:
            str: The extracted search results, getting website URLs from DDG, and using ScrapeGhost to pull their data.
        """
        # This is a placeholder and should be replaced with actual scraping logic, leveraging scrapeghost as defined above
        extracted_results = search_results
        return extracted_results

    def parse_results(self, results):
        # Parse the search results using a Margin AIFunction to
        # This is a placeholder and should be replaced with actual parsing logic

        parsed_results = results
        return parsed_results

    def evaluate_results(self, parsed_results, query):
        # Evaluate the relevance of the parsed results in reference to the user query, using the Marvin AIFunction to assign a score to the utility of the sum of the extracted results.
        # This is a placeholder and should be replaced with actual evaluation logic
        evaluated_results = parsed_results
        return evaluated_results

    def respond_or_search_again(self, evaluated_results):
        # Respond to the user's query or continue the search based on the evaluated results.
        # If the evaluated results are not satisfactory, the agent should continue the search by calling the search function again.
        # If the evaluated results are satisfactory, the agent should respond to the user's query.
        # The agent should also respond to the user's query if the evaluated results are satisfactory but the user has indicated that they would like to continue the search.
        # This is a placeholder and should be replaced with actual response logic
        response = evaluated_results
        return response


__all__ = ["WebSearchAgent"]
