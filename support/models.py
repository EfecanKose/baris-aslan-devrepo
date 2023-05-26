from django.db import models
from django.conf import settings










class Support(models.Model):
    name = models.CharField(max_length=120, verbose_name="İsim", null=True, blank=True)
    email = models.CharField(max_length=120, verbose_name="Email Adress", null=True, blank=True)
    subject = models.CharField(max_length=120, verbose_name="Konu", null=True, blank=True)
    message = models.TextField(verbose_name="Mesaj", null=True, blank=True)

    def __str__(self):
        return self.name


class AdminMessage(models.Model):
    support = models.ForeignKey(Support, on_delete=models.CASCADE)
    message = models.TextField(verbose_name="Mesaj", null=True, blank=True)


