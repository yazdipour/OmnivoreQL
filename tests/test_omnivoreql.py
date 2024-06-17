import os
import unittest
import sys
from dotenv import load_dotenv

# Add the parent directory to the path to import the OmnivoreQL module
current_dir = os.path.dirname(os.path.abspath(__file__))
omnivoreql_dir = os.path.join(current_dir, "..", "omnivoreql")
sys.path.insert(0, omnivoreql_dir)
from omnivoreql import OmnivoreQL, CreateLabelInput


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
        api_token = cls.getEnvVariable("OMNIVORE_API_TOKEN")
        if api_token is None:
            raise ValueError("OMNIVORE_API_TOKEN is not set")
        print(f"OMNIVORE_API_TOKEN: {api_token[:4]}")
        cls.client = OmnivoreQL(api_token)

    @staticmethod
    def getEnvVariable(variable_name):
        for arg in sys.argv[1:]:
            if arg.startswith(variable_name + "="):
                return arg.split("=")[1]
        dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
        load_dotenv(dotenv_path)
        return os.environ.get(variable_name)

    def test_get_profile(self):
        # When
        profile = self.client.get_profile()
        # Then
        self.assertIsNotNone(profile)

    def test_save_url(self):
        # When
        result = self.client.save_url("https://github.com/yazdipour/OmnivoreQL")
        # Then
        self.assertIsNotNone(result)
        self.assertNotIn("errorCodes", result["saveUrl"])
        self.assertTrue(result["saveUrl"]["url"].startswith("http"))

    def test_save_page(self):
        # When
        result = self.client.save_page("http://example.com", "Example")
        # Then
        self.assertIsNotNone(result)
        self.assertNotIn("errorCodes", result["savePage"])

    def test_save_url_with_labels(self):
        # When
        result = self.client.save_url("https://www.google.com", ["test", "google"])
        # Then
        self.assertIsNotNone(result)
        self.assertFalse("errorCodes" in result["saveUrl"])

    def test_get_articles(self):
        # When
        articles = self.client.get_articles()
        # Then
        self.assertIsNotNone(articles)
        self.assertNotIn("errorCodes", articles["search"])
        self.assertGreater(len(articles["search"]["edges"]), 0)

    def test_get_article(self):
        # Given
        username = self.client.get_profile()["me"]["profile"]["username"]
        slug = self.client.get_articles()["search"]["edges"][0]["node"]["slug"]
        # When
        articles = self.client.get_article(username, slug, "markdown")
        # Then
        self.assertIsNotNone(articles)
        self.assertNotIn("errorCodes", articles["article"])
        self.assertIsNotNone(articles["article"]["article"]["id"])

    def test_get_labels(self):
        # When
        labels = self.client.get_labels()
        # Then
        self.assertIsNotNone(labels)
        self.assertNotIn("errorCodes", labels["labels"])

    def test_get_subscriptions(self):
        # When
        subscriptions = self.client.get_subscriptions()
        # Then
        self.assertIsNotNone(subscriptions)
        self.assertNotIn("errorCodes", subscriptions["subscriptions"])

    def test_archive_article(self):
        # Given
        save_result = self.client.save_url("https://pypi.org/project/omnivorex/")
        self.assertIsNotNone(save_result)
        # When
        last_article = self.client.get_articles()["search"]["edges"][0]
        result = self.client.archive_article(last_article["node"]["id"])
        # Then
        self.assertIsNotNone(result)
        self.assertEqual(result["setLinkArchived"]["message"], "link_archived")

    def test_delete_article(self):
        # Given
        save_result = self.client.save_url("https://pypi.org/project/omnivoreql/")
        self.assertIsNotNone(save_result)
        # When
        last_article = self.client.get_articles()["search"]["edges"][0]
        result = self.client.delete_article(last_article["node"]["id"])
        # Then
        self.assertIsNotNone(result)
        self.assertIsNotNone(result["setBookmarkArticle"]["bookmarkedArticle"]["id"])

    def test_create_label(self):
        # Given
        label_name = hash("TestLabel")  # create random label name to avoid conflicts
        label_input = CreateLabelInput(
            name=str(label_name), color="#FF0000", description="label description"
        )
        # When
        result = self.client.create_label(label_input)
        # Then
        self.assertIsNotNone(result)
        self.assertNotIn("errorCodes", result["createLabel"])
        self.assertEqual(result["createLabel"]["label"]["name"], label_input.name)
        self.assertEqual(result["createLabel"]["label"]["color"], label_input.color)
        self.assertEqual(
            result["createLabel"]["label"]["description"], label_input.description
        )

    def test_update_label(self):
        # Given
        label_input = CreateLabelInput(name=hash("TestLabel"), color="#FF0000")
        created_label = self.client.create_label(label_input)
        # When
        new_label_name = f"UpdatedLabel-{label_input.name}"
        result = self.client.update_label(
            label_id=created_label["createLabel"]["label"]["id"],
            name=new_label_name,
            color="#0000FF",
            description="An updated TestLabel",
        )
        # Then
        self.assertIsNotNone(result)
        self.assertNotIn("errorCodes", result["updateLabel"])
        self.assertEqual(result["updateLabel"]["label"]["name"], new_label_name)
        self.assertEqual(result["updateLabel"]["label"]["color"], "#0000FF")
        self.assertEqual(
            result["updateLabel"]["label"]["description"], "An updated TestLabel"
        )

    def test_delete_label(self):
        # Given
        label_input = CreateLabelInput(name=hash("TestLabel"), color="#FF0000")
        created_label = self.client.create_label(label_input)
        # When
        result = self.client.delete_label(
            created_label["createLabel"]["label"]["id"]
        )
        # Then
        self.assertIsNotNone(result)
        self.assertNotIn("errorCodes", result["deleteLabel"])
        self.assertEqual(
            result["deleteLabel"]["label"]["id"],
            created_label["createLabel"]["label"]["id"],
        )

    def test_clean_up_created_labels(self):
        try:
            labels = self.client.get_labels()["labels"]
            for label in labels["labels"]:
                self.client.delete_label(label["id"])
        except Exception as e:
            print(f"Error cleaning up labels: {e}")


if __name__ == "__main__":
    unittest.main()
