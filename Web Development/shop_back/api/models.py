from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    description = models.TextField(max_length=200)
    count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return self.name + ": " + self.description