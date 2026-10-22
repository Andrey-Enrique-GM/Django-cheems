from django.db import models


class UserAccount(models.Model):
    PROFILE_ADMINISTRATOR = 1
    PROFILE_OPERATOR = 2
    PROFILE_CHOICES = [
        (PROFILE_ADMINISTRATOR, "Administrador"),
        (PROFILE_OPERATOR, "Operador"),
    ]

    name = models.CharField(max_length=255)
    account = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    profile = models.PositiveSmallIntegerField(
        choices=PROFILE_CHOICES,
        default=PROFILE_ADMINISTRATOR,
    )

    class Meta:
        db_table = "user"


class WorkOrderRecord(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.PositiveSmallIntegerField(
        choices=[
            (1, "Pendiente"),
            (2, "En Proceso"),
            (3, "Completada"),
        ],
        default=1,
    )

    class Meta:
        db_table = "work_order"


class WorkOrderHistoryRecord(models.Model):
    date = models.DateTimeField()
    id_user = models.PositiveBigIntegerField()
    action = models.PositiveSmallIntegerField()
    id_work_order = models.PositiveBigIntegerField()

    class Meta:
        db_table = "work_order_history"


class LogRecord(models.Model):
    date = models.DateTimeField()
    description = models.TextField()
    id_user = models.PositiveBigIntegerField()
    module = models.PositiveSmallIntegerField()

    class Meta:
        db_table = "log"
