from cookbook.apps.web_search_agent import QueryType, WebSearchAgent
import unittest

from marvin.components.ai_model import AIModel

class TestWebSearchAgent(unittest.TestCase):
    def setUp(self):
        self.agent = WebSearchAgent()

    def test_classify_query(self):
        print("\nRunning test: test_classify_query")
        query = "What's the weather like today?"
        result = self.agent.classify_query(query)
        print(f"Type of result: {type(result)}, Value: {result}")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, QueryType)

    def test_determine_search_requirements(self):
        print("\nRunning test: test_determine_search_requirements")
        live_context = {"chat_log": ["What's the weather like today?", "It's sunny and warm."], 
                        "question": "What's the weather like today?"}
        result = self.agent.determine_search_requirements(live_context)
        print(f"Type of result: {type(result)}, Value: {result}")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

    def test_modify_search_requirements(self):
        print("\nRunning test: test_modify_search_requirements")
        query = "What's the weather like today?"
        search_requirements = {"requirement1": "value1", "requirement2": "value2"}
        results = self.agent.modify_search_requirements(query, search_requirements)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, tuple)
        self.assertEqual(len(results), 2)

    def test_determine_search_requirements(self):
        print("\nRunning test: test_determine_search_requirements")
        live_context = {"chat_log": ["What's the weather like today?", "It's sunny and warm."], 
                        "question": "What's the weather like today?"}
        result = await self.agent.determine_search_requirements(live_context)
        print(f"Type of result: {type(result)}, Value: {result}")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

    def test_extract_results(self):
        print("\nRunning test: test_extract_results")
        search_results = "search results"
        result = await self.agent.extract_results(search_results)
        print(f"Type of result: {type(result)}, Value: {result}")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, AIModel)

    def test_parse_results(self):
        print("\nRunning test: test_parse_results")
        extracted_results = AIModel()
        result = await self.agent.parse_results(extracted_results)
        print(f"Type of result: {type(result)}, Value: {result}")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
    def test_evaluate_results(self):
        print("\nRunning test: test_evaluate_results")
        parsed_results = []
        query = "What's the weather like today?"
        result = self.agent.evaluate_results(parsed_results, query)
        print(f"Type of result: {type(result)}, Value: {result}")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)

    def test_respond_or_search_again(self):
        print("\nRunning test: test_respond_or_search_again")
        evaluated_results = []
        query = "What's the weather like today?"
        live_context = {"chat_log": ["What's the weather like today?", "It's sunny and warm."], 
                        "question": "What's the weather like today?"}
        result = self.agent.respond_or_search_again(evaluated_results, query, live_context)
        print(f"Type of result: {type(result)}, Value: {result}")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)

if __name__ == '__main__':
    unittest.main()