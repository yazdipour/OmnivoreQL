import uuid
import os
from typing import List, Optional
from gql.transport.requests import RequestsHTTPTransport
from gql import gql, Client
from dataclasses import asdict
from .models import CreateLabelInput


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
        self.queries = {}

    def _get_query(self, query_name: str) -> str:
        if query_name not in self.queries:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            query_file_path = os.path.join(current_dir, f"queries/{query_name}.graphql")
            with open(query_file_path, "r") as file:
                self.queries[query_name] = gql(file.read())
        return self.queries[query_name]

    def save_url(
        self,
        url: str,
        labels: Optional[List[str]] = None,
        client_request_id: str = str(uuid.uuid4()),
    ):
        """
        Save a URL to Omnivore.

        :param url: The URL to save.
        :param labels: The labels to assign to the item.
        :param client_request_id: The client request ID.
        """
        labels = [] if labels is None else [{"name": x} for x in labels]
        return self.client.execute(
            self._get_query("SaveUrl"),
            variable_values={
                "input": {
                    "clientRequestId": client_request_id,
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
            self._get_query("SavePage"),
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
        return self.client.execute(self._get_query("Viewer"))

    def get_labels(self):
        """
        Get the labels of the current user.
        """
        return self.client.execute(self._get_query("Labels"))

    def get_subscriptions(self):
        """
        Get the subscriptions of the current user.
        """
        return self.client.execute(self._get_query("GetSubscriptions"))

    def get_articles(
        self,
        limit: int = None,
        after: int = 0,
        format: str = "html",
        query: str = "in:inbox",
        include_content: bool = False,
    ):
        """
        Get articles for the current user. Maximum articles currently you can get is 100. Use 'after' to fetch more.

        :param limit: The number of articles to return (max can be 100).
        :param after: Get articles after this cursor position (Default is 0).
        :param format: The output format of the articles. ('html' [Default], 'markdown')
        :param query: The query to use for filtering articles. Example of query by date: 'in:inbox published:2024-03-01..*'. See https://docs.omnivore.app/using/search.html#filtering-by-save-publish-dates for more information.
        :param include_content: Whether to include the content of the articles.
        """
        return self.client.execute(
            self._get_query("Search"),
            variable_values={
                "first": limit,
                "after": str(after),
                "query": query,
                "format": format,
                "includeContent": include_content,
            },
        )

    def get_article(self, username: str, slug: str, format: str = None, include_content: bool = False):
        """
        Get an article by username and slug.

        :param username: Omnivore username.
        :param slug: The slug of the article.
        :param format: The format of the article to return.
        """
        return self.client.execute(
            self._get_query("ArticleContent"),
            variable_values={
                "username": username,
                "slug": slug,
                "format": format,
                "includeContent": include_content,
            },
        )

    def archive_article(self, article_id: str, to_archive: bool = True):
        """
        Archive or unarchive an article.

        :param article_id: The ID of the article to archive.
        :param to_archive: Whether to archive or unarchive the article.
        """
        return self.client.execute(
            self._get_query("ArchiveSavedItem"),
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
        return self.client.execute(
            self._get_query("DeleteSavedItem"),
            variable_values={"input": {"articleID": article_id, "bookmark": False}},
        )

    def create_label(self, label: CreateLabelInput):
        """
        Create a new label using a dataclass for input.

        :param label: An instance of LabelInput with the label data.
        """
        return self.client.execute(
            self._get_query("CreateLabel"),
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
            self._get_query("UpdateLabel"),
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
            self._get_query("DeleteLabel"),
            variable_values={"id": label_id},
        )

    def set_page_labels(
        self, page_id: str, labels: List[CreateLabelInput]
    ) -> dict:
        """
        Set labels for a page.

        :param page_id: The ID of the page to set labels for.
        :param labels: The labels to set.
        """
        return self.set_page_labels_by_fields(page_id, labels)

    def set_page_labels_by_fields(self, page_id: str, labels: List[dict]) -> dict:
        """
        Set labels for a page.

        :param page_id: The ID of the page to set labels for.
        :param labels: The labels to set.
        """
        parsed_labels = []
        for label in labels:
            if isinstance(label, CreateLabelInput):
                label = asdict(label)
            parsed_labels.append(
                {
                    "name": label["name"],
                    "color": label["color"],
                    "description": label["description"],
                }
            )

        return self.client.execute(
            self._get_query("ApplyLabels"),
            variable_values={
                "input": {
                    "pageId": page_id,
                    "labels": parsed_labels,
                }
            },
        )

    def set_page_labels_by_ids(self, page_id: str, label_ids: List[str]) -> dict:
        """
        Set labels for a page.

        :param page_id: The ID of the page to set labels for.
        :param label_ids: The IDs of the labels to set.
        """
        return self.client.execute(
            self._get_query("ApplyLabels"),
            variable_values={
                "input": {
                    "pageId": page_id,
                    "labelIds": label_ids,
                }
            },
        )
