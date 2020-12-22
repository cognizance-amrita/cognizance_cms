from django.db import models
from adminapp.models import Member


class displayUserNames(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

   
class Application(models.Model):
    departments = (
        ('CSE','CSE'),
        ('CSE(AI)','CSE(AI)'),
        ('CYS','CYS'),
        ('CCE','CCE'),
        ('ECE','ECE')
    )

    domains = (
        ('Cyber Security','Cyber Security'),
        ('Artificial Intelligence','Artificial Intelligence'),
        ('Data Science','Data Science'),
        ('Competitive Programming','Competitive Programming'),
        ('Hackathons','Hackathons'),
        ('Open Source','Open Source')
    )

    years = (
        ('I year', 'I year'),
        ('II year','II year'),
        ('III year','III year'),
        ('IV year','IV year')
    )
    
    statuses = (
        ('Under review','Under review'),
        ('Accepted','Accepted'),
        ('Rejected','Rejected')
    )
    '''
    members = []
    mems = Member.objects.all()

    for m in mems:
        if m.role == 'Administrator':
            members.append((m.fullname,m.fullname))

    members = tuple(members)
    '''
    
    fullname = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=100, null=True)
    department = models.CharField(max_length=100, null=True, choices=departments)
    domain = models.CharField(max_length=100, null=True, choices=domains)
    ques1 = models.TextField(max_length=400, null=True)
    writeup = models.TextField(max_length=1000, null=True)
    ac_year = models.CharField(max_length=20, null=True, choices=years)
    applied_on = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=50, null=True, choices=statuses)
    experience = models.TextField(max_length=500, null=True)
    reviewer = models.OneToOneField(Member,null=True, on_delete=models.SET_NULL)


    def __str__(self):
        return self.fullname
    