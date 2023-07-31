
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


from src.marvin.components.ai_application import AIApplication

class WebSearchAgent:

    description: str = "A custom web search agent"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.search_tool = DuckDuckGoSearch()
        self.ai_application = AIApplication(name="WebSearchAgent", description=self.description)


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


    def determine_search_requirements(self, live_context=None):
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

        # Use the shared AIApplication instance to determine the search requirements based on the live context
        search_requirements = self.ai_application.run(live_context)

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
        modified_query, parameters = ai_function(query, search_requirements)

        return modified_query, parameters
    
    def search_web(self, query, live_context):
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
        search_requirements = self.determine_search_requirements(live_context)
        
        # Modify the query and parameters based on the search requirements
        modified_query, parameters = self.modify_search_requirements(query, search_requirements)

        # Search the web using the DuckDuckGoSearch tool with the modified query and parameters
        search_results = self.search_tool.run(modified_query)
        
        return search_results

    def extract_results(self, search_results):
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
        schema = self.ai_application.run(search_results)

        # Create an instance of the SchemaScraper class with the schema
        scraper = SchemaScraper(schema)

        # Scrape the raw search results
        scraped_data = scraper.scrape(search_results)

        # Convert the scraped data into an instance of an AI model
        extracted_results = AIModelFactory(scraped_data)

        return extracted_results


    def parse_results(self, results):
        # Use AIModel to parse the search results into structured data
        parsed_results = AIModel.extract(results)
        return parsed_results

    def evaluate_results(self, parsed_results, query):
        # Define an AIFunction that evaluates the relevance of a result
        evaluate_relevance = AIFunction(fn=self._evaluate_relevance)
        
        # Use the AIFunction to evaluate the relevance of each result
        evaluated_results = [evaluate_relevance.run(result, query) for result in parsed_results]

        return evaluated_results

    def respond_or_search_again(self, evaluated_results, query, live_context):
        # Create an AIApplication that maintains the state of the conversation or task
        app = AIApplication(name="WebSearchAgent", description="A web search agent")
        
        # Use the AIApplication to decide whether to respond or search again
        decision = app.run(evaluated_results)
        
        if decision == "respond":
            # If the decision is to respond, format the response
            response = self._format_response(evaluated_results)
        else:
            # Otherwise, continue the search
            response = self.search_web(query, live_context)
        
        return response



__all__ = ["WebSearchAgent"]
