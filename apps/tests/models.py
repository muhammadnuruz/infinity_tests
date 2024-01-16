from django.db import models

from apps.topics.models import Topics


class Tests(models.Model):
    question = models.TextField()
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Tests"

    def __str__(self):
        return f"{self.question}"


class Answers(models.Model):
    answer = models.TextField()
    is_correct = models.BooleanField()
    test = models.ForeignKey(Tests, on_delete=models.CASCADE, related_name='answers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"

    def __str__(self):
        return f"{self.answer}-{self.is_correct}"
