import os
import unittest
import sys
from dotenv import load_dotenv

# Add the path to the folder containing the omnivoreql module to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import omnivoreql.omnivoreql as omnivoreql

class TestOmnivoreQL(unittest.TestCase):
    omnivoreql = None

    def setUp(self):
        if self.omnivoreql is None:
            # Put in .env file or use 'python -m unittest test_omnivoreql.py OMNIVORE_API_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
            self.api_token = self.getEnvVariable('OMNIVORE_API_TOKEN')
            print("OMNIVORE_API_TOKEN: " + self.api_token)
            self.omnivoreql = omnivoreql.OmnivoreQL(
                "https://api-prod.omnivore.app/api/graphql", self.api_token)

    def getEnvVariable(self, variable_name):
        for arg in sys.argv[1:]:
            if arg.startswith(variable_name + '='):
                return arg.split('=')[1]
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        return os.environ.get(variable_name)

    def test_get_profile(self):
        profile = self.omnivoreql.get_profile()
        self.assertIsNotNone(profile)

    def test_save_url(self):
        result = self.omnivoreql.save_url("https://www.google.com")
        self.assertIsNotNone(result)
        self.assertFalse('errorCodes' in result['saveUrl'])

    def test_get_articles(self):
        articles = self.omnivoreql.get_articles()
        self.assertIsNotNone(articles)
        self.assertFalse('errorCodes' in articles['search'])

    def test_get_article(self):
        username = self.omnivoreql.get_profile()['me']['profile']['username']
        slug = self.omnivoreql.get_articles()['search']['edges'][0]['node']['slug']
        articles = self.omnivoreql.get_article(
            username, slug
        )
        self.assertIsNotNone(articles)
        self.assertFalse('errorCodes' in articles['article'])

    def test_get_labels(self):
        labels = self.omnivoreql.get_labels()
        self.assertIsNotNone(labels)
        self.assertFalse('errorCodes' in labels['labels'])

    def test_get_subscriptions(self):
        subscriptions = self.omnivoreql.get_subscriptions()
        self.assertIsNotNone(subscriptions)
        self.assertFalse('errorCodes' in subscriptions['subscriptions'])


if __name__ == '__main__':
    unittest.main()
