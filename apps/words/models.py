from django.db import models

from apps.categories.models import Categories


class Words(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='words')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Word"
        verbose_name_plural = "Words"

    def __str__(self):
        return f"{self.name}"
