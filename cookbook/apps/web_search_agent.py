
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

        This method takes a user's query as input and uses the QueryType classifier to determine
        the type of the query. The QueryType classifier categorizes queries into types such as
        FACTUAL_INFORMATION, LATEST_NEWS, GITHUB_PROJECT, API_DOCUMENTATION, DEBUGGING_HELP, etc.

        [Note: QueryType Classifier Spec Defined Below]
            AI Classifier Notes:
            # `ai_classifier` is implemented as a Python decorator that adds additional attributes and methods to an Enum class.

            ### Top-Level Use

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
        [Note AI Classifier Spec Ends Here]
        """
        #TODO check against spec to ensure proper use of the Marvin AiClassifier
        query_type = QueryType(query)

        return query_type

    def determine_search_requirements(self, live_context = {}):
        """
        Determine the search requirements based on the live context.

        Args:
            live_context (dict): The live context containing the chat log/history and the specific question/problem identified by the classifier.

        Returns:
            dict: The search requirements.

        [Note: Marvin AIFunction Spec Defined Below]

            # AIFunction Definition and example

            `AIFunction` is a class that represents a Python function with a signature and docstring as a prompt for an AI to predict the function's output.

            ### Implementation

            `AIFunction` is implemented as a Pydantic `BaseModel` with additional methods for predicting function output.

            ### Top-Level Use

            ```python
            from src.marvin.components.ai_function import ai_fn

            @ai_fn
            def add(a: int, b: int) -> int:
                """Adds two integers."""

            # Predict function output
            result = add(1, 2)
            print(result)  # 3
            ```

            ### Developer Utility

            `AIFunction` provides a way to leverage AI to predict the output of a Python function based on its signature and docstring.
        [Note AIFunction Spec Ends Here]
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

        [Note ]
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

        [Note: Full ScrapeGhost Spec Defined Below]
            # API Reference

            ## `SchemaScraper`

            The `SchemaScraper` class is the main interface to the API.

            It has one required parameter:

            * `schema` - A dictionary describing the shape of the data you wish to extract.

            And the following optional parameters:

            * `models` - *list\[str\]* - A list of models to use, in order of preference.  Defaults to `["gpt-3.5-turbo", "gpt-4"]`.  (See [supported models](../openai/#costs) for details.
            * `model_params` - *dict* - A dictionary of parameters to pass to the underlying GPT model.  (See [OpenAI docs](https://platform.openai.com/docs/api-reference/create-completion) for details.)
            * `max_cost` -  *float* (dollars) - The maximum total cost of calls made using this scraper. This is set to 1 ($1.00) by default to avoid large unexpected charges.
            * `extra_instructions` - *list\[str\]* - Additional instructions to pass to the GPT model as a system prompt.
            * `extra_preprocessors` - *list* - A list of preprocessors to run on the HTML before sending it to the API.  This is in addition to the default preprocessors.
            * `postprocessors` - *list* - A list of postprocessors to run on the results before returning them.  If provided, this will override the default postprocessors.
            * `auto_split_length` - *int* - If set, the scraper will split the page into multiple calls, each of this length. See auto-splitting for details.


            ## `scrape`

            The `scrape` method of a `SchemaScraper` is used to scrape a page.

            ```python
            scraper = SchemaScraper(schema)
            scraper.scrape("https://example.com")
            ```

            * `url_or_html` - The first parameter should be a URL or HTML string to scrape.
            * `extra_preprocessors` - A list of Preprocessors to run on the HTML before sending it to the API.


            It is also possible to call the scraper directly, which is equivalent to calling `scrape`:

            ```python
            scraper = SchemaScraper(schema)
            scraper("https://example.com")
            # same as writing
            scraper.scrape("https://example.com")
            ```

            ## Exceptions

            The following exceptions can be raised by the scraper:

            (all are subclasses of `ScrapeghostError`)

            ### `MaxCostExceeded`

            The maximum cost of the scraper has been exceeded.

            Raise the `max_cost` parameter to allow more calls to be made.

            ### `PreprocessorError`

            A preprocessor encountered an error (such as returning an empty list of nodes).

            ### `TooManyTokens`

            Raised when the number of tokens being sent exceeds the maximum allowed.

            This indicates that the HTML is too large to be processed by the API.

            !!! tip

                Consider using the `css` or `xpath` selectors to reduce the number of tokens being sent, or use the `auto_split_length` parameter to split the request into multiple requests if necessary.

            ### `BadStop`

            Indicates that OpenAI ran out of space before the stop token was reached.

            !!! tip

                OpenAI considers both the input and the response tokens when determining if the token limit has been exceeded.

                If you are using `auto_split_length`, consider decreasing the value to leave more space for responses.

            ### `InvalidJSON`

            Indicates that the JSON returned by the API is invalid.

            # Usage

            ## Data Flow

            Since most of the work is done by the API, the job of a `SchemaScraper` is to make it easier to pass HTML and get valid output.

            If you are going to go beyond the basics, it is important to understand the data flow:

            1. The page HTML is passed through any [preprocessors](#preprocessors).

                a. The `CleanHTML` preprocessor removes unnecessary tags and attributes.  (This is done by default.)

                b. If an `XPath` or `CSS` preprocessor is used, the results are selected and re-combined into a single HTML string.

                c. Custom preprocessors can also execute here.

            2. The HTML and schema are sent to the LLM with instructions to extract.

            3. The results are passed through any [postprocessors](#postprocessors).

                a. The `JSONPostprocessor` converts the results to JSON.  (This is done by default.) If the results are not valid JSON, a second (much smaller) request can be made to ask it to fix the JSON.

                b. Custom postprocessors can also execute here.

            You can modify nearly any part of the process to suit your needs.  (See [Customization](#customization) for more details.)

            ### Auto-splitting

            While the flow above covers most cases, there is one special case that is worth mentioning.

            If you set the `auto_split_length` parameter to a positive integer, the HTML will be split into multiple requests where each
            request aims to be no larger than `auto_split_length` tokens.

            !!! warning

                In **list mode**, a single call can make many requests. Keep an eye on the `max_cost` parameter if you're using this.

                While this seems to work well enough for long lists of similar items, the question of it is worth the time and money is up to you.
                Writing a bit of code is probably the better option in most cases.

            Instead of recombining the results of the `XPath` or `CSS` preprocessor, the results are instead chunked into smaller pieces (<= `auto_split_length`) and sent to the API separately.

            The instructions are also modified slightly, indicating that your schema is for a list of similar items.

            ## Customization

            To make it easier to experiment with different approaches, it is possible to customize nearly every part of the process from how the HTML is retrieved to how the results are processed.

            ### HTTP Requests

            Instead of providing mechanisms to customize the HTTP request made by the library (e.g. to use caching, or make a `POST`), you can simply pass already retrieved HTML to the `scrape` method.

            This means you can use any HTTP library you want to retrieve the HTML.

            ### Preprocessors

            Preprocessors allow you to modify the HTML before it is sent to the API.

            Three preprocessors are provided:

            * `CleanHTML` - Cleans the HTML using `lxml.html.clean.Cleaner`.
            * `XPath` - Applies an XPath selector to the HTML.
            * `CSS` - Applies a CSS selector to the HTML.

            !!! note

                `CleanHTML` is always applied first, as it is part of the default preprocessors list.

            You can add your own preprocessors by passing a list to the `extra_preprocessors` parameter of `SchemaScraper`.

            ```python
            scraper = SchemaScraper(schema, extra_preprocessors=[CSS("table")])
            ```

            It is also possible to pass preprocessors at scrape time:

            ```python
            scraper = SchemaScraper(schema)
            scraper.scrape("https://example.com", extra_preprocessors=[CSS("table")])
            ```

            Implementing your own preprocessor is simple, just create a callable that takes a `lxml.html.HtmlElement` and returns a list of one or more `lxml.html.HtmlElement` objects.  Look at `preprocessors.py` for examples.

            ### Altering the Instructions to GPT

            Right now you can pass additional instructions to GPT by passing a list of strings to the `extra_instructions` parameter of `SchemaScraper`.

            You can also pass `model_params` to pass additional arguments to the API.

            ```python
            schema = {"name": "str", "committees": [], "bio": "str"}
            scraper = SchemaScraper(
                schema,
                models=["gpt-4"],
                extra_instructions=["Put the legislator's bio in the 'bio' field. Summarize it so that it is no longer than 3 sentences."],
            )
            scraper.scrape("https://norton.house.gov/about/full-biography").data
            ```
            ```json
            {'name': 'Representative Eleanor Holmes Norton',
             'committees': [
                'House Subcommittee on Highways and Transit',
                'Committee on Oversight and Reform',
                'Committee on Transportation and Infrastructure'
                ],
              'bio': 'Congresswoman Eleanor Holmes Norton has been serving as the congresswoman for the District of Columbia since 1991. She is the Chair of the House Subcommittee on Highways and Transit and serves on two committees: the Committee on Oversight and Reform and the Committee on Transportation and Infrastructure. Before her congressional service, President Jimmy Carter appointed her to serve as the first woman to chair the U.S. Equal Employment Opportunity Commission.'}
            ```

            These instructions can be useful for refining the results, but they are not required.

            ### Altering the API / Model

            See <https://github.com/jamesturk/scrapeghost/issues/18>

            ## Postprocessors

            Postprocessors take the results of the API call and modify them before returning them to the user.

            Three postprocessors are provided:

            * `JSONPostprocessor` - Converts the results to JSON.
            * `HallucinationChecker` - Checks the results for hallucinations.
            * `PydanticPostprocessor` - Converts the results to JSON and validates them using a `pydantic` model.

            By default, `JSONPostprocessor` and `HallucinationChecker` are enabled.

            `HallucinationChecker` verifies that values in the response are present in the source HTML.  This is useful for ensuring that the results are not "hallucinations".
            This is done as a proof of concept, and to help determine how big of an issue hallucinations are for this use case.

            ### Using `pydantic` Models

            If you want to validate that the returned data isn't just JSON, but data in the format you expect, you can use `pydantic` models.

            ```python
                from pydantic import BaseModel
                from scrapeghost import SchemaScraper, CSS


                class CrewMember(BaseModel):
                    gender: str
                    race: str
                    alignment: str


                # passing a pydantic model to the SchemaScraper # will generate a schema from it
                # and add the PydanticPostprocessor to the postprocessors
                scrape_crewmember = SchemaScraper(schema=CrewMember)
                result = scrape_crewmember.scrape(
                    "https://spaceghost.fandom.com/wiki/Zorak",
                    extra_preprocessors=[CSS(".infobox")],
                )
                print(repr(result.data))
            ```

            ```log
                CrewMember(gender='Male', race='Dokarian', alignment='Evil\\nProtagonist')
            ```

            This works by converting the `pydantic` model to a schema and registering a `PydanticPostprocessor` to validate the results automatically.

            ## Pagination

            One technique to handle pagination is provided by the `PaginatedSchemaScraper` class.

            This class takes a schema that describes a single result, and wraps it in a schema that describes a list of results as well as an additional page.

            For example:

            ```python
            {"first_name": "str", "last_name": "str"}
            ```

            Automatically becomes:

            ```python
            {"next_page": "url", "results": [{"first_name": "str", "last_name": "str"}]}
            ```

            The `PaginatedSchemaScraper` class then takes care of following the `next_page` link until there are no more pages.

            !!! note

                Right now, given the library's stance on customizing requests being "just use your own HTTP library", the `PaginatedSchemaScraper` class does not provide a means to customize the HTTP request used to retrieve the next page.

                If you need a more complicated approach it is recommended you implement your own pagination logic for now,
                <https://github.com/jamesturk/scrapeghost/blob/main/src/scrapeghost/scrapers.py#L238> may be a good starting point.

                If you have strong opinions here, please open an issue to discuss.

            It then takes the combined "results" and returns them to the user.

            Here's a functional example that scrapes several pages of employees:

            ```python
                import json
                from scrapeghost.scrapers import PaginatedSchemaScraper


                schema = {"first_name": "str", "last_name": "str", "position": "str", "url": "url"}
                url = "https://scrapple.fly.dev/staff"

                scraper = PaginatedSchemaScraper(schema)
                resp = scraper.scrape(url)

                # the resulting response is a ScrapeResponse object just like any other
                # all the results are gathered in resp.data
                json.dump(resp.data, open("yoyodyne.json", "w"), indent=2)
            ```

            !!! warning

                One caveat of the current approach: The `url` attribute on a `ScraperResult` from a `PaginatedSchemaScraper` is a semicolon-delimited list of all the URLs that were scraped to produce that result.

        [Note ScrapeGhost Spec Ends Here]
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
        # TODO: Implement the logic to classify the query using the QueryType classifier
        pass

        # TODO: Implement the logic to classify the query using the QueryType classifier
        return query_type

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
