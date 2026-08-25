from django.db import models
from django.contrib.auth.hashers import make_password, check_password


# Create your models here.
class Machine(models.Model):
    name = models.TextField()
    shopId = models.IntegerField()
    creditImage = models.BinaryField(null=True, editable=True)
    gameCash = models.FloatField(null=True)
    assigned = models.BooleanField(default=False)
    getCredit = models.BooleanField(default=False)

class Retail(models.Model):
    name = models.TextField()
    userId = models.IntegerField()
    client = models.TextField()
    cash = models.FloatField(null=True)
    note = models.TextField(null=True)


class Shop(models.Model):
    name = models.TextField()
    userId = models.IntegerField()
    retailId = models.IntegerField(null=True)
    client = models.TextField()
    cash = models.FloatField(null=True)
    cashCredit = models.FloatField(null=True)
    note = models.TextField(null=True)


class User(models.Model):
    username = models.TextField()
    password = models.CharField(max_length=128)
    type = models.TextField()

    def save(self, *args, **kwargs):
        if self.password and not str(self.password).startswith(('pbkdf2_', 'argon2_', 'bcrypt_')):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    def verify_password(self, password):
        return check_password(password, self.password)