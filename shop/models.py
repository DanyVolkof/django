from django.db import models

class Shop(models.Model):
	organization = models.ForeignKey('Organization', on_delete=models.PROTECT)
	name = models.CharField(max_length=100, verbose_name="shop")
	description = models.CharField(max_length=500)
	address = models.CharField(max_length=100)
	index = models.IntegerField()
	is_deleted = models.BooleanField(default=False)


	def __str__(self):
		verbose_name = "shop"
		verbose_name_plural = "shops"
		return self.name




class Organization(models.Model):
	name = models.CharField(max_length=100, verbose_name="organization")
	description = models.CharField(max_length=500)

	def __str__(self):
		verbose_name = "organization"
		verbose_name_plural = "organizations"
		return self.name

