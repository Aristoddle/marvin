from unittest.mock import patch
from cookbook.apps.web_search_agent import QueryType, WebSearchAgent

# Define a constant for the repeated literal
QUERY = "What's the weather like today?"


# Test the classify_query method
def test_classify_query():
    agent = WebSearchAgent()
    query_type = agent.classify_query(QUERY)
    assert isinstance(query_type, QueryType)


# Test the determine_search_requirements method
@patch.object(WebSearchAgent, 'ai_application')
def test_determine_search_requirements(mock_ai_application):
    agent = WebSearchAgent()
    live_context = {
        "chat_log": [QUERY, "It's sunny and warm."], 
        "question": QUERY
    }
    mock_ai_application.run.return_value = {"requirement": "weather"}
    search_requirements = agent.determine_search_requirements(live_context)
    assert search_requirements == {"requirement": "weather"}


# Test the modify_search_requirements method
@patch.object(WebSearchAgent, 'ai_function')
def test_modify_search_requirements(mock_ai_function):
    agent = WebSearchAgent()
    search_requirements = {"requirement": "weather"}
    mock_ai_function.run.return_value = ("modified_query", "parameters")
    
    # Breaking down the line into multiple lines
    modified_query, parameters = agent.modify_search_requirements(
        QUERY, 
        search_requirements
    )    

    assert modified_query == "modified_query"
    assert parameters == "parameters"


# Test the search_web method
@patch.object(WebSearchAgent, 'search_tool')
def test_search_web(mock_search_tool):
    agent = WebSearchAgent()
    live_context = {
        "chat_log": [QUERY, "It's sunny and warm."], 
        "question": QUERY
    }
    mock_search_tool.run.return_value = "search_results"
    search_results = agent.search_web(QUERY, live_context)
    assert search_results == "search_results"