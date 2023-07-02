from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import uuid


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

    def save_url(self, url: str):
        mutation = gql(
            """
            mutation {
                saveUrl(input: { clientRequestId: "%s", source: "api", url: "%s" }) {
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
            % (uuid.uuid4(), url)
        )
        return self.client.execute(mutation)

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

    def search_articles(self, first: int = None, after: int = None, query: str = None):
        q = gql(
            """
            query Search($after: String, $first: Int, $query: String) {
                search(first: $first, after: $after, query: $query) {
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
            q, variable_values={"first": first, "after": after, "query": query}
        )

    def get_articles(self, first: int = None, after: int = None):
        return self.search_articles(first, after)

    def get_article(self, username: str, slug: str, include_friends_highlights: bool = False):
        query = gql(
            """
            query GetArticle($username: String!, $slug: String!, $includeFriendsHighlights: Boolean) {
                article(username: $username, slug: $slug) {
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
                "includeFriendsHighlights": include_friends_highlights,
            },
        )
