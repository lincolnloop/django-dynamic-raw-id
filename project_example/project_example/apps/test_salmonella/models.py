from django.db import models


class SalmonellaTest(models.Model):
    user = models.ForeignKey('auth.User')
