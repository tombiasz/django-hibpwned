from django.db import models


class PwnedPassword(models.Model):

    hash = models.CharField(max_length=40, unique=True, db_index=True)