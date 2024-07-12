import os
import unittest
import sys
from dotenv import load_dotenv
from omnivoreql.omnivoreql import OmnivoreQL
from omnivoreql.models import CreateLabelInput

"""
Unit tests for the OmnivoreQL client.
To run the tests, execute the following command:
    python -m unittest discover -s tests
"""


class TestOmnivoreQL(unittest.TestCase):

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
        print("\nStarting OmnivoreQL tests...\n")
        api_token = cls.getEnvVariable("OMNIVORE_API_TOKEN")
        if api_token is None:
            raise ValueError("OMNIVORE_API_TOKEN is not set")
        print(f"OMNIVORE_API_TOKEN: {api_token[:4]}")
        cls.client = OmnivoreQL(api_token)
        cls.sample_label = None
        # clean_up_created_labels from previous tests
        try:
            labels = cls.client.get_labels()["labels"]
            for label in labels["labels"]:
                if not cls.sample_label:
                    cls.sample_label = label
                    continue
                cls.client.delete_label(label["id"])
        except Exception as e:
            print(f"Error cleaning up labels: {e}")
        if not cls.sample_label:
            cls.sample_label = cls.client.create_label(
                CreateLabelInput(str(hash("test_update_label")), "#FF0000")
            )["createLabel"]["label"]

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
        result = self.client.save_url("https://github.com/yazdipour/OmnivoreQL", ["testLabel"])
        # Then
        self.assertIsNotNone(result)
        self.assertNotIn("errorCodes", result["saveUrl"])
        self.assertTrue(result["saveUrl"]["url"].startswith("http"))

    def test_save_page(self):
        # When
        result = self.client.save_page("http://example.com", "Example", ["label1"])
        # Then
        self.assertIsNotNone(result)
        self.assertNotIn("errorCodes", result["savePage"])

    def test_get_articles(self):
        # When
        articles = self.client.get_articles(include_content=True)
        # Then
        self.assertIsNotNone(articles)
        self.assertNotIn("errorCodes", articles["search"])
        self.assertGreater(len(articles["search"]["edges"]), 0)
        self.assertIsNotNone(articles["search"]["edges"][0]["node"]["id"])
        self.assertIsNotNone(articles["search"]["edges"][0]["node"]["content"])

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
        label_input = CreateLabelInput(
            name=str(hash("test_create_label")), color="#FF0000"
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
        label_sample = self.sample_label
        # When
        new_label_name = f"UpdatedLabel-{hash(label_sample['name'])}"
        result = self.client.update_label(
            label_id=label_sample["id"],
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
        label_sample = self.client.create_label(
            CreateLabelInput(str(hash("test_update_label")), "#FF0000")
        )["createLabel"]["label"]
        # When
        result = self.client.delete_label(label_sample["id"])
        # Then
        self.assertIsNotNone(result)
        self.assertNotIn("errorCodes", result["deleteLabel"])
        self.assertEqual(
            result["deleteLabel"]["label"]["id"],
            label_sample["id"],
        )

    def test_set_page_labels(self):
        # Given
        page = self.client.get_articles(limit=1)["search"]["edges"][0]["node"]
        label_sample = self.sample_label
        created_label_input = CreateLabelInput(
            label_sample["name"],
            label_sample["color"],
            label_sample["description"],
        )
        # When
        result = self.client.set_page_labels(page["id"], [created_label_input])
        # Then
        self.assertIsNotNone(result)
        self.assertNotIn("errorCodes", result["setLabels"])
        self.assertEqual(
            result["setLabels"]["labels"][0]["id"], label_sample["id"]
        )

    def test_set_page_labels_by_ids(self):
        # Given
        page = self.client.get_articles(limit=1)["search"]["edges"][0]["node"]
        label_sample = self.sample_label
        # When
        result = self.client.set_page_labels_by_ids(
            page["id"], label_ids=[label_sample["id"]]
        )
        # Then
        self.assertIsNotNone(result)
        self.assertNotIn("errorCodes", result["setLabels"])
        self.assertEqual(
            result["setLabels"]["labels"][0]["id"], label_sample["id"]
        )


if __name__ == "__main__":
    unittest.main()
