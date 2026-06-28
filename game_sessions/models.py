from django.db import models
from users.models import User
from puzzles.models import Puzzle

class GameSession(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    puzzle      = models.ForeignKey(Puzzle, on_delete=models.CASCADE)
    score       = models.IntegerField(default=0)
    time_taken  = models.IntegerField(default=0)   # seconds
    hints_used  = models.IntegerField(default=0)
    completed   = models.BooleanField(default=False)
    played_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-played_at']

    def __str__(self):
        return f"{self.user.username} - {self.puzzle.type} - {self.score}pts"
