import graphene
import adminapp.api.schema

class Query(adminapp.api.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)