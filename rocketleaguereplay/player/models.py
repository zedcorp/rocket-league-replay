# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class RlMatch(models.Model):
    scoreblue = models.IntegerField(blank=True, null=True)
    scorered = models.IntegerField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    starttime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'rl_match'


class RlPlayer(models.Model):
    name = models.TextField(blank=True, null=True)
    goal = models.IntegerField(blank=True, null=True)
    shot = models.IntegerField(blank=True, null=True)
    assist = models.IntegerField(blank=True, null=True)
    saves = models.IntegerField(blank=True, null=True)
    onlineid = models.TextField(blank=True, null=True)
    platform = models.TextField(blank=True, null=True)
    team = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'rl_player'


class RlTeam(models.Model):

    class Meta:
        managed = True
        db_table = 'rl_team'


class RlUser(models.Model):
    onlineid = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'rl_user'
