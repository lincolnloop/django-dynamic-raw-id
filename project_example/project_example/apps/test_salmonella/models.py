from django.db import models

class SalmonellaTest(models.Model):
    rawid_fk = models.ForeignKey('auth.User', related_name='rawid_fk')
    rawid_fk_limited = models.ForeignKey('auth.User',
        related_name='staff_members', limit_choices_to={'is_staff': True})
    rawid_many = models.ManyToManyField('auth.User',
        related_name='staff_members_many')

    salmonella_fk = models.ForeignKey('auth.User', related_name='salmonella_fk')
    salmonella_fk_limited = models.ForeignKey('auth.User',
        related_name='salmonella_fk_limited', limit_choices_to={'is_staff': True})
    salmonella_many = models.ManyToManyField('auth.User',
        related_name='salmonella_many')