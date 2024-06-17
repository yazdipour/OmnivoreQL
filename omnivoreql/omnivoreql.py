from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import uuid
from models import CreateLabelInput
from dataclasses import asdict
import os
import glob
from typing import List, Optional


class OmnivoreQL:
    def __init__(
        self,
        api_token: str,
        graphql_endpoint_url: str = "https://api-prod.omnivore.app/api/graphql",
    ) -> None:
        """
        Initialize a new instance of the GraphQL client.

        :param api_token: The API token to use for authentication.
        :param graphql_endpoint_url: The URL of the Omnivore GraphQL endpoint.
        """
        transport = RequestsHTTPTransport(
            url=graphql_endpoint_url,
            headers={"content-type": "application/json", "authorization": api_token},
            use_json=True,
        )
        self.client = Client(transport=transport, fetch_schema_from_transport=False)
        self.queries = self._load_queries("queries")

    def _load_queries(self, queries_path: str) -> dict:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        queries_path = os.path.join(current_dir, queries_path)
        queries = {}
        for file in glob.glob(f"{queries_path}/*.graphql"):
            with open(file, "r") as f:
                queries[os.path.basename(file).replace(".graphql", "")] = (
                    f.read().replace("\n", " ")
                )
        return queries

    def save_url(
        self,
        url: str,
        labels: Optional[List[str]] = None,
        clientRequestId: str = str(uuid.uuid4()),
    ):
        """
        Save a URL to Omnivore.

        :param url: The URL to save.
        :param labels: The labels to assign to the item.
        :param clientRequestId: The client request ID.
        """
        labels = [] if labels is None else [{"name": x} for x in labels]
        return self.client.execute(
            gql(self.queries["SaveUrl"]),
            variable_values={
                "input": {
                    "clientRequestId": clientRequestId,
                    "source": "api",
                    "url": url,
                    "labels": labels,
                }
            },
        )

    def save_page(self, url: str, original_content: str, labels: List[str] = None):
        """
        Save a page with html content to Omnivore.

        :param url: The URL of the page to save.
        :param original_content: The original html content of the page.
        :param labels: The labels to assign to the item.
        """
        labels = [] if labels is None else [{"name": x} for x in labels]
        return self.client.execute(
            gql(self.queries["SavePage"]),
            variable_values={
                "input": {
                    "clientRequestId": str(uuid.uuid4()),
                    "source": "api",
                    "url": url,
                    "originalContent": original_content,
                    "labels": labels,
                }
            },
        )

    def get_profile(self):
        """
        Get the profile of the current user.
        """
        return self.client.execute(gql(self.queries["Viewer"]))

    def get_labels(self):
        """
        Get the labels of the current user.
        """
        return self.client.execute(gql(self.queries["Labels"]))

    def get_subscriptions(self):
        """
        Get the subscriptions of the current user.
        """
        return self.client.execute(gql(self.queries["GetSubscriptions"]))

    def get_articles(
        self,
        limit: int = None,
        cursor: str = None,
        format: str = "html",
        query: str = "in:inbox",
        include_content: bool = False,
    ):
        """
        Get articles for the current user.

        :param limit: The number of articles to return.
        :param cursor: The cursor to use for pagination.
        :param format: The output format of the articles. Can be 'html' (default) or 'markdown'.
        :param query: The query to use for filtering articles. Example of query by date: 'in:inbox published:2024-03-01..*'. See https://docs.omnivore.app/using/search.html#filtering-by-save-publish-dates for more information.
        :param include_content: Whether to include the content of the articles.
        """
        return self.client.execute(
            gql(self.queries["Search"]),
            variable_values={
                "first": limit,
                "after": cursor,
                "query": query,
                "format": format,
                "includeContent": include_content,
            },
        )

    def get_article(self, username: str, slug: str, format: str = None):
        """
        Get an article by username and slug.

        :param username: Omnivore username.
        :param slug: The slug of the article.
        :param format: The format of the article to return.
        """
        return self.client.execute(
            gql(self.queries["ArticleContent"]),
            variable_values={
                "username": username,
                "slug": slug,
                "format": format,
            },
        )

    def archive_article(self, article_id: str, to_archive: bool = True):
        """
        Archive or unarchive an article.

        :param article_id: The ID of the article to archive.
        :param to_archive: Whether to archive or unarchive the article.
        """
        return self.client.execute(
            gql(self.queries["ArchiveSavedItem"]),
            variable_values={"input": {"linkId": article_id, "archived": to_archive}},
        )

    def unarchive_article(self, article_id: str):
        """
        Unarchive an article.

        :param article_id: The ID of the article to unarchive.
        """
        return self.archive_article(article_id, False)

    def delete_article(self, article_id: str):
        """
        Delete an article.

        :param article_id: The ID of the article to delete.
        """
        q = self.queries["DeleteSavedItem"]
        return self.client.execute(
            gql(q),
            variable_values={"input": {"articleID": article_id, "bookmark": False}},
        )

    def create_label(self, label: CreateLabelInput):
        """
        Create a new label using a dataclass for input.

        :param label: An instance of LabelInput with the label data.
        """
        return self.client.execute(
            gql(self.queries["CreateLabel"]),
            variable_values={"input": asdict(label)},
        )

    def update_label(
        self, label_id: str, name: str, color: str, description: str = None
    ):
        """
        Update a label.

        :param label_id: The ID of the label to update.
        :param name: The name of the label.
        :param color: The color of the label.
        :param description: The description of the label.
        """
        return self.client.execute(
            gql(self.queries["UpdateLabel"]),
            variable_values={
                "input": {
                    "labelId": label_id,
                    "name": name,
                    "color": color,
                    "description": description,
                }
            },
        )

    def delete_label(self, label_id: str):
        """
        Delete a label.

        :param label_id: The ID of the label to delete.
        """
        return self.client.execute(
            gql(self.queries["DeleteLabel"]),
            variable_values={"id": label_id},
        )
