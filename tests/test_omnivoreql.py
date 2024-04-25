import os
import unittest
import sys
from dotenv import load_dotenv
# Add the path to the folder containing the omnivoreql module to the Python path
sys.path.append(os.path.abspath('../omnivoreql'))
from omnivoreql import OmnivoreQL

class TestOmnivoreQL(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        """
        Set up class method for unit tests of OmnivoreQL.

        This method initializes the OmnivoreQL client with an API token.
        The 'OMNIVORE_API_TOKEN' must be specified either in a '.env' file located in 
        the same directory as this script or passed directly when executing the test script.

        Example command to run tests with an environment variable:
            python -m unittest test_omnivoreql.py OMNIVORE_API_TOKEN='your_api_token_here'

        Raises:
            ValueError: If the 'OMNIVORE_API_TOKEN' is not set.
        """
        api_token = cls.getEnvVariable('OMNIVORE_API_TOKEN')
        if api_token is None:
            raise ValueError("OMNIVORE_API_TOKEN is not set")
        print(f"OMNIVORE_API_TOKEN: {api_token[:4]}")
        cls.client = OmnivoreQL(api_token)

    @staticmethod
    def getEnvVariable(variable_name):
        for arg in sys.argv[1:]:
            if arg.startswith(variable_name + '='):
                return arg.split('=')[1]
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        return os.environ.get(variable_name)

    def test_get_profile(self):
        # When
        profile = self.client.get_profile()
        # Then
        self.assertIsNotNone(profile)

    def test_save_url(self):
        # When
        result = self.client.save_url("https://www.google.com")
        # Then
        self.assertIsNotNone(result)
        self.assertNotIn("errorCodes", result["saveUrl"])

    def test_get_articles(self):
        # When
        articles = self.client.get_articles()
        # Then
        self.assertIsNotNone(articles)
        self.assertNotIn('errorCodes', articles['search'])

    def test_get_article(self):
        # Given
        username = self.client.get_profile()['me']['profile']['username']
        slug = self.client.get_articles()['search']['edges'][0]['node']['slug']
        # When
        articles = self.client.get_article(
            username, slug, 'markdown'
        )
        # Then
        self.assertIsNotNone(articles)
        self.assertNotIn('errorCodes', articles['article'])

    def test_get_labels(self):
        # When
        labels = self.client.get_labels()
        # Then
        self.assertIsNotNone(labels)
        self.assertNotIn('errorCodes', labels['labels'])

    def test_get_subscriptions(self):
        # When
        subscriptions = self.client.get_subscriptions()
        # Then
        self.assertIsNotNone(subscriptions)
        self.assertNotIn('errorCodes', subscriptions['subscriptions'])

    def test_archive_article(self):
        # Given
        save_result = self.client.save_url("https://www.google.com")
        self.assertIsNotNone(save_result)
        # When
        last_article = self.client.get_articles()['search']['edges'][0]
        result = self.client.archive_article(last_article['node']['id'])
        # Then
        self.assertIsNotNone(result)

    def test_delete_article(self):
        # Given
        save_result = self.client.save_url("https://www.google.com")
        self.assertIsNotNone(save_result)
        # When
        last_article = self.client.get_articles()['search']['edges'][0]
        result = self.client.delete_article(last_article['node']['id'])
        # Then
        self.assertIsNotNone(result)
        self.assertIsNotNone(result['setBookmarkArticle']['bookmarkedArticle']['id'])


if __name__ == '__main__':
    unittest.main()
