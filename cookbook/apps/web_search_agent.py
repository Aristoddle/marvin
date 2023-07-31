from marvin import AIApplication
from marvin.tools.web import DuckDuckGoSearch
from src.marvin.components.ai_classifier import ai_classifier
from src.marvin.components.ai_model import AIModel, GitHubRepo, APIDoc
from enum import Enum

@ai_classifier
class QueryType(Enum):
    FACTUAL_INFORMATION = 1
    LATEST_NEWS = 2
    # Add more query types as needed

class CustomWebSearchAgent(WebSearchAgent):
    description: str = "A custom web search agent"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # We can add any additional initialization here

def classify_query(self, query):
    """
    Classify the user's query into predefined categories using the QueryType classifier.

    This method takes a user's query as input and uses the QueryType classifier to determine 
    the type of the query. The QueryType classifier categorizes queries into types such as 
    FACTUAL_INFORMATION, LATEST_NEWS, GITHUB_PROJECT, API_DOCUMENTATION, DEBUGGING_HELP, etc.

    Args:
        query (str): The user's query. This should be a string containing the user's question or request.

    Returns:
        QueryType: The type of the query as determined by the QueryType classifier. This is an enum value that represents the category of the query.
    """
    # Classify the query using the QueryType classifier
    query_type = QueryType(query)
    return query_type
        return query_type

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
