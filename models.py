from django.db import models

# Create your models here.







class Shop(models.Model):
	organization_id = models.ForeignKey('Organization', on_delete=models.PROTECT)
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=500)
	address = models.CharField(max_length=100)
	index = models.IntegerField()
	is_deleted = models.BooleanField(default=False)


	def __str__(self):
		return self.name




class Organization(models.Model):
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=500)

	def __str__(self):
		return self.name





