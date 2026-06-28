from django.db import models
from users.models import User

class Badge(models.Model):
    BADGE_TYPES = [
        ('first_game',    '🎮 First Game',        ),
        ('streak_3',      '🔥 3-Day Streak',      ),
        ('streak_7',      '⚡ 7-Day Streak',      ),
        ('streak_30',     '👑 30-Day Streak',     ),
        ('score_100',     '💯 Score 100',         ),
        ('score_1000',    '🚀 Score 1000',        ),
        ('speed_demon',   '⚡ Speed Demon',       ),
        ('perfectionist', '✨ Perfect Solve',     ),
        ('brain_master',  '🧠 Brain Master',      ),
    ]

    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge_type = models.CharField(max_length=30, choices=[(b[0], b[1]) for b in BADGE_TYPES])
    earned_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge_type')

    def __str__(self):
        return f"{self.user.username} - {self.badge_type}"

def check_and_award_badges(user, session=None):
    """Auto-award badges based on user stats"""
    awarded = []

    def award(badge_type):
        badge, created = Badge.objects.get_or_create(user=user, badge_type=badge_type)
        if created:
            awarded.append(badge_type)

    if user.total_games >= 1:        award('first_game')
    if user.current_streak >= 3:     award('streak_3')
    if user.current_streak >= 7:     award('streak_7')
    if user.current_streak >= 30:    award('streak_30')
    if user.brain_score >= 100:      award('score_100')
    if user.brain_score >= 1000:     award('score_1000')
    if session and session.time_taken <= 30 and session.completed:
        award('speed_demon')
    if session and session.hints_used == 0 and session.completed:
        award('perfectionist')
    if user.brain_score >= 5000:     award('brain_master')

    return awarded
