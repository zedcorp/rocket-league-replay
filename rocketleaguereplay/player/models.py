# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class RlMatch(models.Model):
    rlmatchid = models.TextField(blank=False, unique=True)
    scoreblue = models.IntegerField(blank=False, null=False)
    scorered = models.IntegerField(blank=False, null=False)
    duration = models.IntegerField(blank=False, null=False)
    starttime = models.DateTimeField(blank=False, null=False)
    frames = models.TextField(blank=True, unique=False)
    replayjson =  models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'rl_match'

class RlTeam(models.Model):
    class Meta:
        managed = True
        db_table = 'rl_team'


class RlUser(models.Model):
    onlineid = models.TextField(blank=False, null=False, unique=True)
    name = models.TextField(blank=False, null=False)
    nbmatchs = models.IntegerField(blank=False, null=False, default=0)
    nbwin = models.IntegerField(blank=False, null=False, default=0)
    nblose = models.IntegerField(blank=False, null=False, default=0)
    pwin = models.FloatField(blank=False, null=False, default=0)
    score = models.IntegerField(blank=False, null=False, default=0)
    pscore = models.FloatField(blank=False, null=False, default=0)
    nbgoal = models.IntegerField(blank=False, null=False, default=0)
    pgoal = models.FloatField(blank=False, null=False, default=0)
    nbassist = models.IntegerField(blank=False, null=False, default=0)
    passist = models.FloatField(blank=False, null=False, default=0)
    nbsave = models.IntegerField(blank=False, null=False, default=0)
    psave = models.FloatField(blank=False, null=False, default=0)

    class Meta:
        managed = True
        db_table = 'rl_user'

class RlPlayer(models.Model):
    idmatch = models.ForeignKey(RlMatch, on_delete=models.CASCADE)
    userid = models.ForeignKey(RlUser, on_delete=models.CASCADE)
    name = models.TextField(blank=False, null=False, default=0)
    score = models.IntegerField(blank=False, null=False, default=0)
    goal = models.IntegerField(blank=False, null=False, default=0)
    shot = models.IntegerField(blank=False, null=False, default=0)
    assist = models.IntegerField(blank=False, null=False, default=0)
    saves = models.IntegerField(blank=False, null=False, default=0)
    platform = models.TextField(blank=False, null=False, default=0)
    team = models.IntegerField(blank=False, null=False, default=0)

    class Meta:
        managed = True
        db_table = 'rl_player'
        unique_together = ("idmatch", "userid")
        
class RlMatchEvent(models.Model):

      
    idmatch = models.ForeignKey(RlMatch, on_delete=models.CASCADE)
    userid = models.ForeignKey(RlUser, on_delete=models.CASCADE)
    time = models.FloatField(blank=False, null=False, default=0)
    type = models.TextField(blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'rl_match_event'