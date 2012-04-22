from django.db import models

class SalmonellaTest(models.Model):
    user = models.ForeignKey('auth.User')
    staff_member = models.ForeignKey('auth.User',
        related_name='staff_members', limit_choices_to={'is_staff': True})
    staff_member_many = models.ManyToManyField('auth.User',
        related_name='staff_members_many')