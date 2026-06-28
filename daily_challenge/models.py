from django.db import models
from puzzles.models import Puzzle

class DailyChallenge(models.Model):
    date   = models.DateField(unique=True)
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE)

    def __str__(self):
        return f"Daily Challenge {self.date}"
