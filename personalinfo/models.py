# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Admin(models.Model):
    a_id = models.CharField(primary_key=True, max_length=20)
    a_password = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin'


class Classes(models.Model):
    u = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    classes = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'classes'


class Covarea(models.Model):
    location = models.CharField(max_length=200, blank=True, null=True)
    s_time = models.DateTimeField(blank=True, null=True)
    e_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'covarea'


class DailyClock(models.Model):
    u = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)
    qrcode = models.CharField(db_column='QRcode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    emergency_person = models.CharField(max_length=20, blank=True, null=True)
    emergency_phone = models.CharField(max_length=20, blank=True, null=True)
    c_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'daily_clock'


class Dormitory(models.Model):
    u = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    department = models.IntegerField(blank=True, null=True)
    room_id = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dormitory'


class Healthcode(models.Model):
    u = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    healthcode = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'healthcode'


class Interfacciami(models.Model):
    u = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    reason = models.CharField(max_length=200, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'interfacciami'


class Iotable(models.Model):
    u = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    in_out = models.IntegerField(blank=True, null=True)
    io_time = models.DateTimeField(blank=True, null=True)
    door_id = models.CharField(max_length=20, blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'iotable'


class Judge(models.Model):
    u = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    l_time = models.IntegerField(blank=True, null=True)
    reason = models.CharField(max_length=200, blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    situation = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'judge'


class NucleicAcid(models.Model):
    u = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    t_time = models.DateTimeField(blank=True, null=True)
    result = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nucleic_acid'


class Passphrase(models.Model):
    u = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    passphrase = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'passphrase'


class Quarantine(models.Model):
    u = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    q_location = models.CharField(max_length=200, blank=True, null=True)
    cancel_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'quarantine'


class TQuarantine(models.Model):
    u = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    q_location = models.CharField(max_length=200, blank=True, null=True)
    i_time = models.DateTimeField(blank=True, null=True)
    o_time = models.DateTimeField(blank=True, null=True)
    t_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_quarantine'


class USchedule(models.Model):
    u = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    o_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'u_schedule'


class Users(models.Model):
    u_id = models.CharField(primary_key=True, max_length=20)
    u_name = models.CharField(max_length=50, blank=True, null=True)
    u_password = models.CharField(max_length=20, blank=True, null=True)
    identity = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
