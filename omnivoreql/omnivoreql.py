from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import uuid
from typing import List

class OmnivoreQL:
    def __init__(self, api_token: str, graphqlEndpointUrl: str = "https://api-prod.omnivore.app/api/graphql") -> None:
        """
        Initialize a new instance of the GraphQL client.

        :param url: The URL of the Omnivore GraphQL endpoint.
        :param api_token: The API token to use for authentication.
        """
        transport = RequestsHTTPTransport(url=graphqlEndpointUrl,
                                          headers={
                                              "content-type": "application/json",
                                              "authorization": api_token
                                          },
                                          use_json=True)
        self.client = Client(transport=transport,
                             fetch_schema_from_transport=False)

    def save_url(self, url: str, labels: List[str] = None):
        labels = [] if labels is None else [{"name": x} for x in labels]
        mutation = gql(
            """
            mutation SaveUrl($input: SaveUrlInput!) {
                saveUrl(input: $input) {
                    ... on SaveSuccess {
                        url
                        clientRequestId
                    }
                    ... on SaveError {
                        errorCodes
                        message
                    }
                }
            }
        """
        )
        return self.client.execute(
            mutation,
            variable_values = {
                "clientRequestId": str(uuid.uuid4()),
                "source": "api",
                "url": url,
                "labels": labels
            }
        )

    def get_profile(self):
        query = gql(
            """
            query Viewer {
            me {
                id
                name
                isFullUser
                profile {
                id
                username
                pictureUrl
                bio
                }
            }
            }
        """
        )
        return self.client.execute(query)

    def get_labels(self):
        query = gql(
            """
            query GetLabels { 
                labels {
                    ... on LabelsSuccess {
                    labels {
                        ...LabelFields
                    }
                    }
                    ... on LabelsError {
                    errorCodes
                    }
                }
            }
            fragment LabelFields on Label {
                id
                name
                color
                description
                createdAt
            }"""
        )
        return self.client.execute(query)

    def get_subscriptions(self):
        query = gql(
            """
                query GetSubscriptions {
                subscriptions(sort: { by: UPDATED_TIME }) {
                    ... on SubscriptionsSuccess {
                    subscriptions {
                        id
                        name
                        newsletterEmail
                        url
                        description
                        status
                        unsubscribeMailTo
                        unsubscribeHttpUrl
                        createdAt
                        updatedAt
                    }
                    }
                    ... on SubscriptionsError {
                    errorCodes
                    }
                }
                }
            """
        )
        return self.client.execute(query)

    def get_articles(self, limit: int = None, cursor: str = None, format: str = 'markdown', query: str = "in:inbox", include_content: bool = False):
        q = gql(
            """
            query Search($after: String, $first: Int, $query: String, $format: String, $includeContent: Boolean) {
                search(after: $after, first: $first, query: $query, format: $format, includeContent: $includeContent) {
                    ... on SearchSuccess {
                        edges {
                            cursor
                            node {
                                id
                                title
                                slug
                                url
                                pageType
                                contentReader
                                createdAt
                                isArchived
                                readingProgressPercent
                                readingProgressTopPercent
                                readingProgressAnchorIndex
                                author
                                image
                                description
                                publishedAt
                                ownedByViewer
                                originalArticleUrl
                                uploadFileId
                                labels {
                                    id
                                    name
                                    color
                                }
                                pageId
                                shortId
                                quote
                                annotation
                                state
                                siteName
                                subscription
                                readAt
                                savedAt
                                wordsCount
                                recommendations {
                                    id
                                    name
                                    note
                                    user {
                                        userId
                                        name
                                        username
                                        profileImageURL
                                    }
                                    recommendedAt
                                }
                                highlights {
                                    ...HighlightFields
                                }
                            }
                        }
                        pageInfo {
                            hasNextPage
                            hasPreviousPage
                            startCursor
                            endCursor
                            totalCount
                        }
                    }
                    ... on SearchError {
                        errorCodes
                    }
                }
            }
            
            fragment HighlightFields on Highlight {
                id
                type
                shortId
                quote
                prefix
                suffix
                patch
                annotation
                createdByMe
                createdAt
                updatedAt
                sharedAt
                highlightPositionPercent
                highlightPositionAnchorIndex
                labels {
                    id
                    name
                    color
                    createdAt
                }
            }
        """
        )
        return self.client.execute(
            q, variable_values={
                "first": limit, "after": cursor, "query": query, "format": format, "includeContent": include_content}
        )

    def get_article(self, username: str, slug: str, format: str = None, include_friends_highlights: bool = False):
        query = gql(
            """
            query GetArticle($username: String!, $slug: String!, $format: String, $includeFriendsHighlights: Boolean) {
                article(username: $username, slug: $slug, format: $format) {
                    ... on ArticleSuccess {
                        article {
                            ...ArticleFields
                            content
                            highlights(input: { includeFriends: $includeFriendsHighlights }) {
                                ...HighlightFields
                            }
                            labels {
                                ...LabelFields
                            }
                            recommendations {
                                ...RecommendationFields
                            }
                        }
                    }
                    ... on ArticleError {
                        errorCodes
                    }
                }
            }
            
            fragment ArticleFields on Article {
                id
                title
                url
                author
                image
                savedAt
                createdAt
                publishedAt
                contentReader
                originalArticleUrl
                readingProgressPercent
                readingProgressTopPercent
                readingProgressAnchorIndex
                slug
                isArchived
                description
                linkId
                state
                wordsCount
            }

            fragment HighlightFields on Highlight {
                id
                type
                shortId
                quote
                prefix
                suffix
                patch
                annotation
                createdByMe
                createdAt
                updatedAt
                sharedAt
                highlightPositionPercent
                highlightPositionAnchorIndex
                labels {
                    id
                    name
                    color
                    createdAt
                }
            }

            fragment LabelFields on Label {
                id
                name
                color
                description
                createdAt
            }

            fragment RecommendationFields on Recommendation {
                id
                name
                note
                user {
                    userId
                    name
                    username
                    profileImageURL
                }
                recommendedAt
            }
        """
        )
        return self.client.execute(
            query,
            variable_values={
                "username": username,
                "slug": slug,
                "format": format,
            },
        )

    def archive_article(self, article_id: str, toArchive: bool = True):
        mutation = gql(
            """
        mutation SetLinkArchived($input: ArchiveLinkInput!) {
            setLinkArchived(input: $input) {
                    ... on ArchiveLinkSuccess {
                        linkId
                        message
                    }
                    ... on ArchiveLinkError {
                        errorCodes
                        message
                    }
                }
            }
        """)
        return self.client.execute(
            mutation,
            variable_values={
                "input": {
                    "linkId": article_id,
                    "archived": toArchive
                }
            }
        )

    def unarchive_article(self, article_id: str):
        return self.archive_article(article_id, False)

    def delete_article(self, article_id: str):
        mutation = gql("""
            mutation SetBookmarkArticle($input: SetBookmarkArticleInput!) {
                setBookmarkArticle(input: $input) {
                    ... on SetBookmarkArticleSuccess {
                        bookmarkedArticle {
                            id
                        }
                    }
                    ... on SetBookmarkArticleError {
                        errorCodes
                    }
                }
            }""")
        return self.client.execute(
            mutation,
            variable_values= {
                "input": {
                    "articleID": article_id,
                    "bookmark": False
                }
            }
        )
