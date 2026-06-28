from django.db import models

class User(models.Model):
    """
    Custom user model — NOT extending AbstractUser.
    We use Firebase for auth, so we just store profile data here.
    """
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(unique=True)
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
