from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class MyApp(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='my_apps')

    def __str__(self):
        return f'MyApp {self.id} {self.name}'

    class Meta:
        verbose_name_plural = 'my apps'
        ordering = ['name']
