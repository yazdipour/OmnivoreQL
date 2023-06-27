import os
import unittest
from omnivoreql import OmnivoreQL


class TestOmnivoreQL(unittest.TestCase):

    OMNIVORE_API_URL = os.environ.get("OMNIVORE_API_URL", "https://api-prod.omnivore.app/api/graphql")
    OMNIVORE_API_TOKEN = os.environ.get("OMNIVORE_API_TOKEN")

    def setUp(self):
        self.omnivoreql = OmnivoreQL(
            self.OMNIVORE_API_URL, self.OMNIVORE_API_TOKEN)

    def test_get_user(self):
        user = self.omnivoreql.get_user()
        assert user

    def test_get_profile(self):
        profile = self.omnivoreql.get_profile()
        assert profile

    def test_save_url(self):
        result = self.omnivoreql.save_url("https://www.google.com")
        assert result

    def test_get_articles(self):
        articles = self.omnivoreql.get_articles()
        assert articles

    def test_get_article(self):
        articles = self.omnivoreql.get_article(
            "yazdipour", "how-to-pick-a-random-element-from-an-infinite-stream-188ac853c09"
        )
        assert articles

    def test_get_labels(self):
        labels = self.omnivoreql.get_labels()
        assert labels

    def test_get_label(self):
        label = self.omnivoreql.get_label("python")
        assert label


if __name__ == '__main__':
    unittest.main()
