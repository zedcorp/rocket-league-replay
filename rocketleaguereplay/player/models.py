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

    class Meta:
        managed = True
        db_table = 'rl_user'

class RlPlayer(models.Model):
    idmatch = models.ForeignKey(RlMatch, on_delete=models.CASCADE)
    userid = models.ForeignKey(RlUser, on_delete=models.CASCADE)
    name = models.TextField(blank=False, null=False)
    goal = models.IntegerField(blank=False, null=False)
    shot = models.IntegerField(blank=False, null=False)
    assist = models.IntegerField(blank=False, null=False)
    saves = models.IntegerField(blank=False, null=False)
    platform = models.TextField(blank=False, null=False)
    team = models.IntegerField(blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'rl_player'
        unique_together = ("idmatch", "userid")