from django.db import models

# Create your models here.

class Review(models.Model):
    restaurant_name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    review_text = models.TextField()
    sentiment = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.restaurant_name}"
