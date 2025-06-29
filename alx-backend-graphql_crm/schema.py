import graphene

class Query(graphene.ObjectType):
    """
    Main Query class that serves as the entry point for all GraphQL queries.
    This class defines the available query fields and their corresponding resolvers.
    """

    hello = graphene.String()

    def resolve_hello(root, info):
        return "Hello, GraphQL!"

# GraphQL schema that combines all queries, mutations, and subscriptions
schema = graphene.Schema(query=Query)
