from django.db import models


class File(models.Model):
    name = models.CharField(max_length=50, verbose_name='file_name', unique=True)
    data = models.TextField(verbose_name='file_content')
