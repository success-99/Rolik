from datetime import timedelta

from django.db import models

# Create your models here.

GREEN, RED, WHITE = ("green", "red", "white")
STARTED, GOING_ON, FINISHED = ("started", "going_on", "finished")


class Rolik(models.Model):
    COLORS_CHOICES = (
        (GREEN, GREEN),
        (RED, RED),
        (WHITE, WHITE)
    )

    rolik_num = models.CharField(max_length=50, unique=True)
    rolik_size = models.CharField(max_length=50)
    rolik_color = models.CharField(max_length=30, choices=COLORS_CHOICES, default=WHITE)

    def __str__(self):
        return str(self.rolik_num)


class InRolik(models.Model):
    STATUS = (
        (STARTED, STARTED),
        (GOING_ON, GOING_ON),
        (FINISHED, FINISHED)
    )
    rolik = models.ForeignKey(Rolik, related_name='inrolik', on_delete=models.CASCADE)
    roliktime = models.DateTimeField(null=True, blank=True)
    rolik_pay = models.PositiveIntegerField(default=10000)
    status = models.CharField(max_length=20, choices=STATUS, default=FINISHED)

    def __str__(self):
        return str(self.status)
