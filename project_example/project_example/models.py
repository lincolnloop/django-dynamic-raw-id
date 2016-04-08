from django.db import models

class DirectPrimaryKeyModel(models.Model):
    num = models.IntegerField("Number", primary_key=True)

    def __str__(self):
        return str(self.num)

class CharPrimaryKeyModel(models.Model):
    chr = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.chr

class SalmonellaTest(models.Model):
    rawid_fk = models.ForeignKey('auth.User',
        related_name='rawid_fk', blank=True, null=True)

    rawid_fk_limited = models.ForeignKey('auth.User',
        related_name='rawid_fk_limited',
        limit_choices_to={'is_staff': True},
        blank=True, null=True)

    rawid_many = models.ManyToManyField('auth.User',
        related_name='rawid_many', blank=True)

    rawid_fk_direct_pk = models.ForeignKey(DirectPrimaryKeyModel,
        related_name='rawid_fk_direct_pk', blank=True, null=True)

    salmonella_fk = models.ForeignKey('auth.User',
        related_name='salmonella_fk', blank=True, null=True)

    salmonella_fk_limited = models.ForeignKey('auth.User',
        related_name='salmonella_fk_limited',
        limit_choices_to={'is_staff': True},
        blank=True, null=True)

    salmonella_many = models.ManyToManyField('auth.User',
        related_name='salmonella_many', blank=True)

    salmonella_fk_direct_pk = models.ForeignKey(DirectPrimaryKeyModel,
        related_name='salmonella_fk_direct_pk', blank=True, null=True)

    salmonella_fk_char_pk = models.ForeignKey(CharPrimaryKeyModel,
            related_name='salmonella_fk_char_pk', blank=True, null=True)
