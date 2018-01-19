from django.db import models
from django.utils.six import python_2_unicode_compatible


@python_2_unicode_compatible
class DirectPrimaryKeyModel(models.Model):
    num = models.IntegerField("Number", primary_key=True)

    def __str__(self):
        return str(self.num)


@python_2_unicode_compatible
class CharPrimaryKeyModel(models.Model):
    chr = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.chr


@python_2_unicode_compatible
class TestModel(models.Model):
    rawid_fk = models.ForeignKey('auth.User',
        related_name='rawid_fk', blank=True, null=True,
        on_delete=models.CASCADE)

    rawid_fk_limited = models.ForeignKey('auth.User',
        related_name='rawid_fk_limited',
        limit_choices_to={'is_staff': True},
        blank=True, null=True,
        on_delete=models.CASCADE)

    rawid_many = models.ManyToManyField('auth.User',
        related_name='rawid_many', blank=True)

    rawid_fk_direct_pk = models.ForeignKey(DirectPrimaryKeyModel,
        related_name='rawid_fk_direct_pk', blank=True, null=True,
        on_delete=models.CASCADE)

    dynamic_raw_id_fk = models.ForeignKey('auth.User',
        related_name='dynamic_raw_id_fk', blank=True, null=True,
        on_delete=models.CASCADE)

    dynamic_raw_id_fk_limited = models.ForeignKey('auth.User',
        related_name='dynamic_raw_id_fk_limited',
        limit_choices_to={'is_staff': True},
        blank=True, null=True,
        on_delete=models.CASCADE)

    dynamic_raw_id_many = models.ManyToManyField('auth.User',
        related_name='dynamic_raw_id_many', blank=True)

    dynamic_raw_id_fk_direct_pk = models.ForeignKey(DirectPrimaryKeyModel,
        related_name='dynamic_raw_id_fk_direct_pk', blank=True, null=True,
        on_delete=models.CASCADE)

    dynamic_raw_id_fk_char_pk = models.ForeignKey(CharPrimaryKeyModel,
            related_name='dynamic_raw_id_fk_char_pk', blank=True, null=True,
            on_delete=models.CASCADE)

    def __str__(self):
        if self.dynamic_raw_id_fk:
            return self.dynamic_raw_id_fk.username
        return 'Unnamed Test Instance'
