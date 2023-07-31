
from marvin.tools.web import DuckDuckGoSearch
from src.marvin.components.ai_classifier import ai_classifier
from src.marvin.components.ai_model import AIModel, GitHubRepo, APIDoc
from enum import Enum


@ai_classifier
class QueryType(Enum):
    FACTUAL_INFORMATION = 1
    LATEST_NEWS = 2
    GITHUB_PROJECT = 3
    API_DOCUMENTATION = 4
    DEBUGGING_HELP = 5

class WebSearchAgent(WebSearchAgent):

    description: str = "A custom web search agent"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # We can add any additional initialization here

    def classify_query(self, query):
        """
        Classify the user's query into predefined categories using the QueryType classifier.
        """
        # Use the QueryType classifier to classify the user's query
        query_type = QueryType(query)

        # Return the name of the classified query type
        return query_type.name

    def determine_search_requirements(self, live_context = {}):
        """
        Determine the search requirements based on the live context.

        Args:
            live_context (dict): The live context containing the chat log/history and the specific question/problem identified by the classifier.

        Returns:
            dict: The search requirements.
        """
        # TODO: Implement the logic to determine the search requirements based on the live_context, if present, using Marvin's AIFunction tool.
        search_requirements = {}
        return search_requirements

    def modify_search_requirements(self, query, search_requirements) = {}:
        """
        Modify the query and parameters based on the search requirements.

        Args:
            query (str): The user's query.
            search_requirements (dict): The search requirements.

        Returns:
            tuple: The modified query and parameters.
        """

        # TODO: Implement the logic to modify the query and parameters based on the search_requirements using Marvin's AiFunction tool.
        modified_query = query
        parameters = {}
        return modified_query, parameters

    def search_web(self, query, live_context = {}):
        # Search the web using the DuckDuckGoSearch tool
        """
         Search the web based on the user's query and the live context using the DuckDuckGoSearch tool

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
        self.search_tool = DuckDuckGoSearch()
        search_results = self.search_tool.run(query)
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


class CustomWebSearchAgent(WebSearchAgent):
    description: str = "A custom web search agent"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # We can add any additional initialization here

    def classify_query(self, query):
        # Use the QueryType classifier to classify the user's query
        query_type = QueryType(query)
        # Return the name of the classified query type
        return query_type.name

    def determine_search_requirements(self, live_context):
        """
        Determine the search requirements based on the live context.

        Args:
            live_context (dict): The live context containing the chat log/history and the specific question/problem identified by the classifier.

        Returns:
            dict: The search requirements.
        """
        # TODO: Implement the logic to determine the search requirements based on the live_context
        search_requirements = {}
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
        # TODO: Implement the logic to modify the query and parameters based on the search_requirements
        modified_query = query
        parameters = {}
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
        search_results = self.search_tool.run(modified_query, parameters)
        
        return search_results

    def parse_results(self, results):
        # Parse the search results using the GitHubRepo and APIDoc models
        # This is a placeholder and should be replaced with actual parsing logic
        parsed_results = results
        return parsed_results

    def evaluate_results(self, parsed_results):
        # Evaluate the relevance of the parsed results using a classifier
        # This is a placeholder and should be replaced with actual evaluation logic
        evaluated_results = parsed_results
        return evaluated_results

    def respond_or_search_again(self, evaluated_results):
        # Respond to the user's query or continue the search based on the evaluated results
        # This is a placeholder and should be replaced with actual response logic
        response = evaluated_results
        return response


__all__ = ["WebSearchAgent"]
