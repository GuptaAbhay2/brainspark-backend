from django.db import models

class Puzzle(models.Model):
    TYPES = [
        ('sudoku', 'Sudoku'),
        ('speed_math', 'Speed Math'),
        ('logic', 'Logic Puzzle'),
        ('memory', 'Memory Match'),
    ]
    DIFFICULTIES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    type        = models.CharField(max_length=20, choices=TYPES)
    difficulty  = models.CharField(max_length=10, choices=DIFFICULTIES, default='easy')
    # puzzle data stored as JSON — flexible for all game types
    data        = models.JSONField()
    solution    = models.JSONField()
    hint_text   = models.TextField(blank=True)  # pre-written hint
    time_limit  = models.IntegerField(default=0)  # seconds, 0 = no limit
    max_score   = models.IntegerField(default=100)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['type', 'difficulty']

    def __str__(self):
        return f"{self.type} - {self.difficulty} (id:{self.id})"
