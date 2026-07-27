from django.contrib import admin
from django.urls import path
from users import views as user_views
from puzzles import views as puzzle_views
from game_sessions import views as session_views
from leaderboard import views as lb_views
from daily_challenge import views as dc_views
from ai_hints import views as hint_views
from badges import views as badge_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth — username + password
    path('api/users/register/',          user_views.register),
    path('api/users/login/',  user_views.login),
    path('api/users/profile/<int:user_id>/', user_views.get_profile),
    path('api/users/by-email/',          user_views.get_user_by_email),

    # Puzzles
    path('api/puzzles/',                 puzzle_views.get_puzzles),
    path('api/puzzles/all/',             puzzle_views.get_all_puzzles),
    path('api/puzzles/verify/',          puzzle_views.verify_solution),

    # Game sessions
    path('api/sessions/submit/',         session_views.submit_score),
    path('api/sessions/history/<int:user_id>/', session_views.user_history),

    # Leaderboard
    path('api/leaderboard/global/',      lb_views.global_leaderboard),
    path('api/leaderboard/weekly/',      lb_views.weekly_leaderboard),
    path('api/leaderboard/rank/<int:user_id>/', lb_views.user_rank),

    # Daily challenge
    path('api/daily/',                   dc_views.get_today),

    # AI Hints
    path('api/hints/',                   hint_views.get_hint),

    # Badges
    path('api/badges/<int:user_id>/',    badge_views.user_badges),
]
