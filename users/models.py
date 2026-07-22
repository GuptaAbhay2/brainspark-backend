from django.db import models

class User(models.Model):
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(unique=True, blank=True, null=True)
    password_hash   = models.CharField(max_length=64, blank=True, default='')
    avatar          = models.CharField(max_length=10, default='🧠')
    brain_score     = models.IntegerField(default=0)
    total_games     = models.IntegerField(default=0)
    current_streak  = models.IntegerField(default=0)
    longest_streak  = models.IntegerField(default=0)
    last_played     = models.DateField(null=True, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-brain_score']

    def __str__(self):
        return f"{self.username} (Score: {self.brain_score})"
