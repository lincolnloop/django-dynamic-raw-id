from django.db import models


# Test custom forms of primary key fields
class IntPrimaryKeyModel(models.Model):
    num = models.IntegerField("Number", primary_key=True)

    def __str__(self) -> str:
        return str(self.num)


class CharPrimaryKeyModel(models.Model):
    chr = models.CharField(max_length=20, primary_key=True)

    def __str__(self) -> str:
        return str(self.chr)


class UUIDPrimaryKeyModel(models.Model):
    uuid = models.UUIDField(primary_key=True)

    def __str__(self) -> str:
        return str(self.uuid)


class ModelToTest(models.Model):
    # Regular RawID Fields -------------------------------------------------------------
    rawid_fk = models.ForeignKey(
        "auth.User",
        related_name="rawid_fk",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    rawid_fk_limited = models.ForeignKey(
        "auth.User",
        related_name="rawid_fk_limited",
        limit_choices_to={"is_staff": True},
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    rawid_many = models.ManyToManyField(
        "auth.User", related_name="rawid_many", blank=True
    )

    # Dynamic RawID Fields with Django Default PK --------------------------------------
    dynamic_raw_id_fk = models.ForeignKey(
        "auth.User",
        related_name="dynamic_raw_id_fk",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    dynamic_raw_id_fk_limited = models.ForeignKey(
        "auth.User",
        related_name="dynamic_raw_id_fk_limited",
        limit_choices_to={"is_staff": True},
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    dynamic_raw_id_many = models.ManyToManyField(
        "auth.User", related_name="dynamic_raw_id_many", blank=True
    )

    # Dynamic RawID Fields with Custom PK Fields ---------------------------------------
    # Custom PrimaryKey Field Model with a Integer value
    dynamic_raw_id_fk_int_pk = models.ForeignKey(
        IntPrimaryKeyModel,
        related_name="dynamic_raw_id_fk_int_pk",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    # Custom PrimaryKey Field Model with a Character value
    dynamic_raw_id_fk_char_pk = models.ForeignKey(
        CharPrimaryKeyModel,
        related_name="dynamic_raw_id_fk_char_pk",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    # Custom PrimaryKey Field Model with an UUID value
    dynamic_raw_id_fk_uuid_pk = models.ForeignKey(
        UUIDPrimaryKeyModel,
        related_name="dynamic_raw_id_fk_uuid_pk",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        if self.dynamic_raw_id_fk:
            return str(self.dynamic_raw_id_fk)
        if self.dynamic_raw_id_fk_int_pk:
            return str(self.dynamic_raw_id_fk_int_pk)
        if self.dynamic_raw_id_fk_char_pk:
            return str(self.dynamic_raw_id_fk_char_pk)
        if self.dynamic_raw_id_fk_uuid_pk:
            return str(self.dynamic_raw_id_fk_uuid_pk)
        return "Test Instance"
