from django.db import models

# Create your models here.
class Test(models.Model):
	test = models.CharField(max_length=128)

class Key(models.Model):
	user = models.CharField(max_length=128)
	app = models.CharField(max_length=128)
	key = models.CharField(max_length=256)