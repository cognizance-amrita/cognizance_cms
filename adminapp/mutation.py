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
        
class CreateMember(graphene.Mutation):
	
	class Arguments:
		Member = graphene.String()
	
	Member = graphene.Fied(MemberType)
	
	def mutate(self, info, member):
		Member = MemberType(member=Member)
		return CreateMember(member=Member)
        
class Mutations(graphene.ObjectType):
	create_Member = CreateMember.Field()
        
        
     schema = graphene.Schema(query=Query, mutation=Mutations)
     
     result = schema.execute(
     '''
     mutation CreateMember {
     	CreateMember{Member : "Sanjay"}{
     		Member {
     			Membertype
     			}
     		}
     	}
     	'''
     	)
  items = dict(result.data.items())
  print(json.dumps(items, indent=4))
     

