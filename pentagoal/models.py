from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Liga(models.Model):
    name = models.CharField(max_length=15)
    country = models.CharField(max_length=15)

    def __str__(self) -> str:
        return self.name

class Teams(models.Model):
    name = models.CharField(max_length=15)
    goal_scored = models.IntegerField(blank = True,default=0)
    goal_lost = models.IntegerField(blank = True,default=0)
    score = models.IntegerField(blank = True,default=0)
    league = models.ForeignKey(Liga,related_name='league',on_delete=models.DO_NOTHING,null=True)

    def __str__(self) -> str:
        return self.name
    

class Matches(models.Model):
    date = models.DateField()
    time = models.TimeField()
    home_team = models.ForeignKey(Teams,related_name='home_team',on_delete=models.CASCADE)
    home_team_score = models.IntegerField(blank=True,default=0)
    away_team = models.ForeignKey(Teams,related_name='away_team',on_delete=models.CASCADE)
    away_team_score = models.IntegerField(blank=True,default=0)
    matches_league = models.ForeignKey(Liga,related_name='match_league',on_delete=models.DO_NOTHING,null=True)
    def __str__(self) -> str:
        return f'{self.home_team} vs {self.away_team} {self.time}'

@receiver(post_save,sender = Matches)
def post_save_match(sender,instance,created,*args,**kwargs):
    if created:
        league = Teams.objects.filter(name=instance.home_team.name).values("league")[0]['league']
        
        
        # ADD score to overal scored goal of HOME team  
        team_overal_goal = Teams.objects.filter(name=instance.home_team.name).values("goal_scored")[0]["goal_scored"]+instance.home_team_score
        Teams.objects.filter(name=instance.home_team.name,league = league).update(goal_scored = team_overal_goal)

        # LOST goal of HOME team
        minus_goal_team_home = Teams.objects.filter(name=instance.home_team.name).values("goal_lost")[0]["goal_lost"] + instance.away_team_score
        Teams.objects.filter(name=instance.home_team.name,league = league).update(goal_lost = minus_goal_team_home)

        # ADD score to overal scored goal of AWAY team 
        away_team_overal_goal = Teams.objects.filter(name=instance.away_team.name).values("goal_scored")[0]["goal_scored"]+instance.away_team_score
        Teams.objects.filter(name=instance.away_team.name,league = league).update(goal_scored = away_team_overal_goal)

        # LOST goal of AWAY team
        minus_goal_team_home = Teams.objects.filter(name=instance.away_team.name).values("goal_lost")[0]["goal_lost"] + instance.home_team_score
        Teams.objects.filter(name=instance.away_team.name,league = league).update(goal_lost = minus_goal_team_home)

