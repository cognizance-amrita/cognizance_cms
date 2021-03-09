import graphene
from graphene_django import DjangoObjectType
from adminapp.models import Member

class MemberType(DjangoObjectType):
    class Meta:
        model = Member

class Query(graphene.ObjectType):
    members = graphene.List(MemberType)

    def resolve_members(self, info, **kwargs):
        return Member.objects.all()