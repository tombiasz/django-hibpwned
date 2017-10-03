from django.db import models


class PwnedPassword(models.Model):

    hash = models.CharField(max_length=40, db_index=True)