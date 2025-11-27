import graphene


class TestQuery(graphene.ObjectType):
    hello = graphene.String(description="A typical hello world")

    def resolve_hello(root, info):
        return "Hello, World!"
